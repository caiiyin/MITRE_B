import csv, sys
from collections import Counter, OrderedDict
src, out = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(src, encoding="utf-8")))
merged = OrderedDict(); miss = []
for r in rows:
    if not r["raw_ref"]:
        miss.append(r); continue
    k = (r["rt_time"], r["user"], r["src_computer"], r["dst_computer"], r["raw_ref"])
    if k in merged:
        merged[k]["match_on"] = ";".join(sorted(set(merged[k]["match_on"].split(";") + [r["match_on"]])))
    else:
        merged[k] = dict(r)
with open(out, "w", newline="", encoding="utf-8") as o:
    w = csv.DictWriter(o, fieldnames=rows[0].keys()); w.writeheader()
    for r in merged.values(): w.writerow(r)
    for r in miss: w.writerow(r)
keys = Counter((r["rt_time"], r["user"], r["src_computer"], r["dst_computer"]) for r in merged.values())
print("일치한 조합:", len(keys), "/ auth 줄(중복 제거):", len(merged))
print("조합당 auth 줄 수:", dict(sorted(Counter(keys.values()).items())))
print("match_on:", dict(Counter(r["match_on"] for r in merged.values())))
print("인증 방향:", dict(Counter(r["orientation"] for r in merged.values())))
print("인증 방식:", dict(Counter(r["auth_type"] for r in merged.values())))
print("결과:", dict(Counter(r["status"] for r in merged.values())))
print("불일치", len(miss), "개:")
for r in miss: print("   ", r["rt_time"], r["user"], r["src_computer"], "->", r["dst_computer"])
