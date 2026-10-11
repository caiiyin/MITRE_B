"""
트랙 B 2주차(시나리오 정의) 도구

사용법 (PowerShell):
  python week2_tools.py redteam-summary <redteam.txt.gz> [--out <요약.csv>]
  python week2_tools.py grep <파일(.gz/.zip/일반)> <검색어> [<검색어> ...] [--max 20] [--all]
  python week2_tools.py apt29-steps <apt29.xlsx> --day day1 --out <타임라인.csv>
  python week2_tools.py fill-ids <타임라인.csv>
  python week2_tools.py timeline-template <타임라인.csv> --dataset <이름> --scenario <이름> [--rows 10]

grep: 검색어가 모두 들어 있는 줄(--all) 또는 하나라도 들어 있는 줄(기본)을 찾아,
      시각·호스트·이벤트 번호와 검색어 주변 글자를 보여준다. 대소문자 구분 없음.
"""
import argparse
import collections
import csv
import gzip
import io
import json
import sys
import zipfile

TIMELINE_COLUMNS = [
    "dataset_id", "scenario_id", "stage_no", "step", "tactic", "technique_id", "technique_name",
    "start_utc", "end_utc", "actor_user", "actor_ip", "host", "evidence_source", "evidence_query", "notes",
]

TIME_KEYS = ["@timestamp", "UtcTime", "timestamp", "ts", "_time", "EventTime", "time"]
HOST_KEYS = ["Hostname", "Computer", "ComputerName", "host", "@system", "dvc"]
ID_KEYS = ["EventID", "EventCode", "event_type", "@stream", "sourcetype"]


def setup_output():
    try:
        sys.stdout.reconfigure(errors="replace")
        sys.stderr.reconfigure(errors="replace")
    except AttributeError:
        pass


def iter_lines(path):
    """(원본 이름, 줄 문자열)을 차례로 돌려준다. .gz, .zip, 일반 텍스트 모두 지원."""
    p = str(path)
    if p.lower().endswith(".zip"):
        with zipfile.ZipFile(p) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                with z.open(info) as f:
                    for raw in io.TextIOWrapper(f, encoding="utf-8", errors="replace"):
                        yield info.filename, raw
    elif p.lower().endswith(".gz"):
        with gzip.open(p, "rt", encoding="utf-8", errors="replace") as f:
            for raw in f:
                yield p, raw
    else:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            for raw in f:
                yield p, raw


def pick(d, keys):
    for k in keys:
        if k in d and d[k] not in (None, "", "none"):
            return str(d[k])
    return ""


def redteam_summary(args):
    users, srcs, dsts = collections.Counter(), collections.Counter(), collections.Counter()
    per_day = collections.Counter()
    first, last = {}, {}
    total, lo, hi = 0, None, None
    for _, line in iter_lines(args.path):
        parts = line.strip().split(",")
        if len(parts) < 4:
            continue
        t, user, src, dst = int(parts[0]), parts[1], parts[2], parts[3]
        total += 1
        lo = t if lo is None else min(lo, t)
        hi = t if hi is None else max(hi, t)
        users[user] += 1
        srcs[src] += 1
        dsts[dst] += 1
        per_day[t // 86400 + 1] += 1
        first[user] = min(first.get(user, t), t)
        last[user] = max(last.get(user, t), t)

    print(f"레드팀 이벤트 수: {total:,}")
    print(f"시각 범위(초): {lo} ~ {hi}  →  {lo // 86400 + 1}일차 ~ {hi // 86400 + 1}일차")
    print(f"고유 사용자: {len(users)}명, 출발 컴퓨터: {len(srcs)}대, 도착 컴퓨터: {len(dsts)}대")
    print("\n일차별 이벤트 수")
    for day in sorted(per_day):
        print(f"  {day:3d}일차  {per_day[day]:6,}건")
    print("\n출발 컴퓨터 (많은 순)")
    for c, n in srcs.most_common(10):
        print(f"  {c:12s} {n:6,}건")
    print("\n사용자 (많은 순, 상위 15명)")
    for u, n in users.most_common(15):
        print(f"  {u:20s} {n:6,}건  처음 {first[u]}  마지막 {last[u]}")

    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["user", "events", "first_time", "last_time", "first_day", "last_day"])
            for u, n in users.most_common():
                w.writerow([u, n, first[u], last[u], first[u] // 86400 + 1, last[u] // 86400 + 1])
        print(f"\n사용자별 요약을 저장했습니다: {args.out}")


def grep(args):
    words = [w.lower() for w in args.words]
    shown = matched = 0
    earliest = latest = None
    for name, line in iter_lines(args.path):
        low = line.lower()
        hit = all(w in low for w in words) if args.all else any(w in low for w in words)
        if not hit:
            continue
        matched += 1
        t = h = eid = ""
        try:
            d = json.loads(line)
            if isinstance(d, dict) and isinstance(d.get("result"), dict):
                d = d["result"]  # BOTS(Splunk 내보내기) 형식
            if isinstance(d, dict):
                t, h, eid = pick(d, TIME_KEYS), pick(d, HOST_KEYS), pick(d, ID_KEYS)
        except ValueError:
            t = line[:23]  # 텍스트 로그는 앞부분에 시각이 있는 경우가 많음
        if t:
            earliest = t if earliest is None or t < earliest else earliest
            latest = t if latest is None or t > latest else latest
        if shown >= args.max:
            continue
        shown += 1
        w0 = next((w for w in words if w in low), words[0])
        i = low.find(w0)
        ctx = line[max(0, i - 60): i + 100].replace("\n", " ").replace("\r", " ")
        print(f"[{shown}] 시각={t}  호스트={h}  이벤트={eid}")
        print(f"     …{ctx}…")
    print(f"\n일치한 줄: {matched:,}개 (화면에는 최대 {args.max}개 표시)")
    if earliest:
        print(f"일치한 줄 중 가장 이른 시각: {earliest}")
        print(f"일치한 줄 중 가장 늦은 시각: {latest}")
        print("(시각 형식이 섞여 있으면 이 두 값은 참고만 하세요)")


def apt29_steps(args):
    try:
        from openpyxl import load_workbook
    except ImportError:
        print("openpyxl이 필요합니다. 먼저 실행하세요: python -m pip install openpyxl", file=sys.stderr)
        sys.exit(1)
    ws = load_workbook(args.path, read_only=True)[args.day]
    rows = list(ws.iter_rows(values_only=True))
    out = []
    for r in rows[1:]:
        if not r or r[2] is None:
            continue
        stage, techs, step, desc, _hands_on, user, src, tgt = (list(r) + [None] * 8)[:8]
        step = str(step).strip()
        if step == "0":
            continue  # 환경 준비 단계는 공격이 아님
        first_line = str(desc or "").strip().splitlines()[0][:150] if desc else ""
        for tech in str(techs or "").replace("\n", ",").split(","):
            tech = tech.strip()
            if not tech or tech == "None":
                continue
            out.append({
                "dataset_id": "apt29", "scenario_id": args.day, "stage_no": step.split(".")[0],
                "step": step, "tactic": str(stage or "").strip(), "technique_id": "",
                "technique_name": tech, "start_utc": "", "end_utc": "",
                "actor_user": str(user or "").strip(), "actor_ip": "",
                "host": f"{str(src or '').strip()} -> {str(tgt or '').strip()}",
                "evidence_source": "", "evidence_query": "", "notes": first_line,
            })
    with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=TIMELINE_COLUMNS)
        w.writeheader()
        w.writerows(out)
    steps = sorted({o["step"] for o in out}, key=lambda s: (int(s.split(".")[0]), s))
    print(f"{len(steps)}개 단계, {len(out)}개 Technique 행을 저장했습니다: {args.out}")


# 2020년 APT29 에뮬레이션 계획의 예전 ATT&CK 이름 → 현재 ID, 현재 이름
OLD_NAME_TO_ID = {
    "user execution": ("T1204.002", "Malicious File"),
    "masquerading": ("T1036.002", "Right-to-Left Override"),
    "uncommonly used port": ("T1571", "Non-Standard Port"),
    "command-line interface": ("T1059.003", "Windows Command Shell"),
    "powershell": ("T1059.001", "PowerShell"),
    "file and directory discovery": ("T1083", "File and Directory Discovery"),
    "automated collection": ("T1119", "Automated Collection"),
    "data from local system": ("T1005", "Data from Local System"),
    "data compressed": ("T1560", "Archive Collected Data"),
    "data encrypted": ("T1560", "Archive Collected Data"),
    "exfiltration over command and control channel": ("T1041", "Exfiltration Over C2 Channel"),
    "exfiltration over alternative protocol": ("T1048", "Exfiltration Over Alternative Protocol"),
    "remote file copy": ("T1105", "Ingress Tool Transfer"),
    "obfuscated files or information": ("T1027", "Obfuscated Files or Information"),
    "software packing": ("T1027.002", "Software Packing"),
    "deobfuscate/decode files or information": ("T1140", "Deobfuscate/Decode Files or Information"),
    "component object model hijacking": ("T1546.015", "Component Object Model Hijacking"),
    "bypass user account control": ("T1548.002", "Bypass User Account Control"),
    "standard application layer protocol": ("T1071", "Application Layer Protocol"),
    "modify registry": ("T1112", "Modify Registry"),
    "process discovery": ("T1057", "Process Discovery"),
    "file deletion": ("T1070.004", "File Deletion"),
    "system owner/user discovery": ("T1033", "System Owner/User Discovery"),
    "system information discovery": ("T1082", "System Information Discovery"),
    "remote system discovery": ("T1018", "Remote System Discovery"),
    "new service": ("T1543.003", "Windows Service"),
    "service execution": ("T1569.002", "Service Execution"),
    "registry run keys / startup folder": ("T1547.001", "Registry Run Keys / Startup Folder"),
    "credentials in files": ("T1552.001", "Credentials In Files"),
    "private keys": ("T1552.004", "Private Keys"),
    "credential dumping": ("T1003", "OS Credential Dumping"),
    "screen capture": ("T1113", "Screen Capture"),
    "clipboard data": ("T1115", "Clipboard Data"),
    "input capture": ("T1056", "Input Capture"),
    "windows remote management": ("T1021.006", "Windows Remote Management"),
    "windows admin shares": ("T1021.002", "SMB/Windows Admin Shares"),
    "valid accounts": ("T1078", "Valid Accounts"),
    "data staged": ("T1074.001", "Local Data Staging"),
    "system network configuration discovery": ("T1016", "System Network Configuration Discovery"),
    "security software discovery": ("T1518.001", "Security Software Discovery"),
    "permission groups discovery": ("T1069", "Permission Groups Discovery"),
    "execution through api": ("T1106", "Native API"),
    # Day2에 나오는 이름
    "process injection": ("T1055", "Process Injection"),
    "windows management instrumentation event subscription": ("T1546.003", "Windows Management Instrumentation Event Subscription"),
    "ntfs file attributes": ("T1564.004", "NTFS File Attributes"),
    "virtualization/sandbox evasion": ("T1497", "Virtualization/Sandbox Evasion"),
    "peripheral device discovery": ("T1120", "Peripheral Device Discovery"),
    "timestomp": ("T1070.006", "Timestomp"),
    "query registry": ("T1012", "Query Registry"),
    "windows management instrumentation": ("T1047", "Windows Management Instrumentation"),
    "email collection": ("T1114", "Email Collection"),
    "web service": ("T1102", "Web Service"),
    "rundll32": ("T1218.011", "Rundll32"),
    "pass the ticket": ("T1550.003", "Pass the Ticket"),
    "create account": ("T1136", "Create Account"),
}
DEPRECATED = {"commonly used port", "standard cryptographic protocol", "standard non-application layer protocol"}


def fill_ids(args):
    with open(args.path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    filled, deprecated, unknown = 0, 0, collections.Counter()
    for r in rows:
        if r.get("technique_id"):
            continue
        key = " ".join((r.get("technique_name") or "").lower().split())
        if key in OLD_NAME_TO_ID:
            tid, new_name = OLD_NAME_TO_ID[key]
            r["technique_id"] = tid
            if new_name.lower() != key:
                note = f"현재 이름: {new_name}"
                r["notes"] = (note + " / " + r["notes"]) if r.get("notes") else note
            filled += 1
        elif key in DEPRECATED:
            if "ATT&CK에서 폐지됨" in (r.get("notes") or ""):
                continue
            r["notes"] = ("ATT&CK에서 폐지됨 / " + r["notes"]) if r.get("notes") else "ATT&CK에서 폐지됨"
            deprecated += 1
        elif key:
            unknown[r["technique_name"]] += 1
    with open(args.path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=TIMELINE_COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"ID를 채운 행: {filled}개, 폐지된 기법으로 표시한 행: {deprecated}개")
    if unknown:
        print("대응표에 없어 직접 찾아야 하는 이름 (attack.mitre.org에서 검색):")
        for name, n in unknown.most_common():
            print(f"  {name}  ({n}행)")


def timeline_template(args):
    with open(args.path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=TIMELINE_COLUMNS)
        w.writeheader()
        for i in range(1, args.rows + 1):
            w.writerow({"dataset_id": args.dataset, "scenario_id": args.scenario, "stage_no": i})
    print(f"빈 타임라인 양식({args.rows}행)을 만들었습니다: {args.path}")


def main():
    setup_output()
    p = argparse.ArgumentParser(description="트랙 B 2주차 도구")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("redteam-summary", help="LANL redteam 파일 요약")
    a.add_argument("path")
    a.add_argument("--out")
    a.set_defaults(func=redteam_summary)

    a = sub.add_parser("grep", help="검색어가 든 이벤트의 시각·호스트 보기")
    a.add_argument("path")
    a.add_argument("words", nargs="+")
    a.add_argument("--max", type=int, default=20)
    a.add_argument("--all", action="store_true", help="검색어가 모두 들어 있어야 일치")
    a.set_defaults(func=grep)

    a = sub.add_parser("apt29-steps", help="APT29 에뮬레이션 계획을 타임라인 양식 CSV로 내보내기")
    a.add_argument("path")
    a.add_argument("--day", default="day1", choices=["day1", "day2"])
    a.add_argument("--out", required=True)
    a.set_defaults(func=apt29_steps)

    a = sub.add_parser("fill-ids", help="예전 ATT&CK 이름을 보고 technique_id를 자동으로 채우기")
    a.add_argument("path")
    a.set_defaults(func=fill_ids)

    a = sub.add_parser("timeline-template", help="빈 정답 타임라인 양식 만들기")
    a.add_argument("path")
    a.add_argument("--dataset", required=True)
    a.add_argument("--scenario", required=True)
    a.add_argument("--rows", type=int, default=10)
    a.set_defaults(func=timeline_template)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()