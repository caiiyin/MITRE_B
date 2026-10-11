import gzip, json, sys
from collections import Counter
path = sys.argv[1]
rows, skipped = [], []
with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
    for n, line in enumerate(f, 1):
        try:
            r = json.loads(line).get("result")
        except Exception:
            r = None
        if r and "_raw" in r:
            rows.append(r)
        else:
            skipped.append((n, line[:120].strip()))
print("읽은 줄:", len(rows), "/ 건너뛴 줄:", len(skipped))
for n, s in skipped[:3]:
    print("  건너뜀", n, ":", s)
r = rows[0]
print("raw :", r["_raw"][:20])
print("time:", r.get("_time"))
print("키  :", sorted(k for k in r if not k.startswith(("_", "date_"))))
print("토큰 수:", dict(Counter(len(x["_raw"].split()) for x in rows)))
d = sorted(x["_raw"][:10] for x in rows)
print("날짜:", d[0], "~", d[-1])
print("날짜별:", dict(Counter(d)))
