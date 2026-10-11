import gzip, re, csv, sys
from datetime import datetime, timedelta
from collections import Counter
data, events = sys.argv[1], sys.argv[2]
want = {}
for r in csv.DictReader(open(events, encoding="utf-8")):
    f, n = r["raw_ref"].rsplit(":", 1)
    if "Sysmon" in f: want[int(n)] = r["label"]
want.setdefault(591269, "(팀원 예시 줄)")
tp = re.compile(rb'"_time"\s*:\s*"([^"]{19})'); up = re.compile(rb"UtcTime\D{0,12}(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)")
ec = re.compile(rb'"EventCode"\s*:\s*"(\d+)"')
diff = Counter(); byec = Counter(); bylab = Counter(); ex = {}
fn = "botsv1.XmlWinEventLog-Microsoft-Windows-Sysmon-Operational.json.gz"
with gzip.open(data + "\\" + fn, "rb") as f:
    for n, line in enumerate(f, 1):
        a, u = tp.search(line), up.search(line)
        if not (a and u): continue
        d = round(((datetime.strptime(u.group(1).decode(), "%Y-%m-%d %H:%M:%S") - datetime.strptime(a.group(1).decode(), "%Y-%m-%d %H:%M:%S")).total_seconds() - 6*3600) / 60)
        e = ec.search(line); e = e.group(1).decode() if e else "?"
        if d != 0:
            byec[e] += 1
            if n in want: bylab[want[n]] += 1
        diff[d] += 1
        if n in want and (n == 591269 or d != 0) and len(ex) < 5: ex[n] = (e, a.group(1).decode(), u.group(1).decode(), d)
print("UtcTime - (_time+6h), 분 단위 분포(상위):", diff.most_common(8))
print("어긋난 줄의 EventCode:", dict(byec.most_common(6)))
print("라벨 줄 중 어긋난 수:", dict(bylab))
for n, v in ex.items(): print("  줄", n, "EventCode", v[0], "_time", v[1], "UtcTime", v[2], "차이(분)", v[3])
