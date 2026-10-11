import gzip, csv, re, sys
from datetime import datetime, timedelta
from collections import defaultdict, Counter
data, out, timelines = sys.argv[1], sys.argv[2], sys.argv[3:]
FILES = {"suricata": "botsv1.suricata.json.gz",
         "sysmon": "botsv1.XmlWinEventLog-Microsoft-Windows-Sysmon-Operational.json.gz",
         "iis": "botsv1.iis.json.gz",
         "wineventlog-security": "botsv1.WinEventLog-Security.json.gz"}
def utc(s):
    return datetime.strptime(s[:19].replace("T", " "), "%Y-%m-%d %H:%M:%S")
jobs = defaultdict(list); all_labels = []
for tl in timelines:
    for r in csv.DictReader(open(tl, encoding="utf-8-sig")):
        if not r["start_utc"]: continue
        label = "%s:%s:%s" % (r["scenario_id"], r["stage_no"], r["technique_id"])
        all_labels.append(label)
        srcs = [s.strip().lower() for s in r["evidence_source"].split(";")]
        qs = [q.strip() for q in r["evidence_query"].split(" / ")]
        if len(qs) != len(srcs): qs = [r["evidence_query"]] * len(srcs)
        st, en = utc(r["start_utc"]) - timedelta(seconds=1), utc(r["end_utc"]) + timedelta(seconds=1)
        for s, q in zip(srcs, qs):
            if s not in FILES: print("알 수 없는 소스:", s, label); continue
            jobs[FILES[s]].append((label, q.split(), st, en))
tpat = re.compile(rb'"_time"\s*:\s*"([^"]+)"')
fs = re.compile(rb'"flow\.start"\s*:\s*"([^"]+)"'); fe = re.compile(rb'"flow\.end"\s*:\s*"([^"]+)"')
hits = {}; per = Counter()
for fname, stages in jobs.items():
    print("읽는 중:", fname, "(단계", len(stages), "개)", flush=True)
    words = [[w.encode() for w in ws] for _, ws, _, _ in stages]
    with gzip.open(data + "\\" + fname, "rb") as f:
        for n, line in enumerate(f, 1):
            for (label, _, st, en), ws in zip(stages, words):
                if not all(w in line for w in ws): continue
                m = tpat.search(line)
                if not m: continue
                t = utc(m.group(1).decode()) + timedelta(hours=6)
                a, b = fs.search(line), fe.search(line)
                if a and b:   # Suricata flow: 연결 구간이 단계 시간과 겹치면 포함 (원문 -0600 → +6시간)
                    t0 = utc(a.group(1).decode()) + timedelta(hours=6)
                    t1 = utc(b.group(1).decode()) + timedelta(hours=6)
                    if t1 < t0: t0, t1 = t1, t0
                    ok = t0 <= en and t1 >= st
                else:
                    ok = st <= t <= en
                if not ok: continue
                ref = "bots_v1/%s:%d" % (fname, n)
                h = hits.setdefault(ref, {"time": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "source": fname, "labels": []})
                if label not in h["labels"]: h["labels"].append(label); per[label] += 1
with open(out, "w", newline="", encoding="utf-8") as o:
    w = csv.writer(o); w.writerow(["raw_ref", "time_utc", "source", "label"])
    for ref, h in sorted(hits.items(), key=lambda x: (x[1]["time"], x[0])):
        w.writerow([ref, h["time"], h["source"], ";".join(h["labels"])])
multi = Counter(";".join(h["labels"]) for h in hits.values() if len(h["labels"]) > 1)
for label in sorted(set(all_labels), key=lambda x: (x.split(":")[0], int(x.split(":")[1]))):
    print("  %-40s %7d %s" % (label, per[label], "  <-- 0건!" if per[label] == 0 else ""))
print("\n이벤트 수:", len(hits))
print("여러 단계에 걸친 줄:", dict(multi))
print("저장:", out)
