import json, sys
from collections import Counter, defaultdict
path, out = sys.argv[1], sys.argv[2]
cnt = Counter(); fields = defaultdict(Counter); ex = defaultdict(dict)
fmt = "?"; tsv_path = None; tsv_fields = []
with open(path, encoding="utf-8", errors="ignore", newline="") as f:
    lines = f.read().split("\n")
for l in lines:
    l = l.rstrip("\r")
    if not l: continue
    if l.startswith("{"):
        fmt = "JSON"
        try: d = json.loads(l)
        except Exception: continue
        g = d.get("_path") or d.get("@stream") or d.get("log_type") or "?"
        rec = d
    elif l.startswith("#"):
        fmt = "TSV"
        p = l.split("\t")
        if p[0] == "#path": tsv_path = p[1]
        if p[0] == "#fields": tsv_fields = p[1:]
        continue
    else:
        g = tsv_path or "?"
        rec = dict(zip(tsv_fields, l.split("\t")))
    cnt[g] += 1
    for k, v in rec.items():
        if isinstance(v, (dict, list)): v = json.dumps(v)[:60]
        fields[g][k] += 1
        if k not in ex[g] and v not in ("", "-", None): ex[g][k] = str(v)[:60]
with open(out, "w", encoding="utf-8") as o:
    o.write("# 필드 목록: combined_zeek.log (형식 %s, %d줄)\n\n" % (fmt, len(lines)))
    for g, n in cnt.most_common():
        o.write("## %s (%d건)\n\n| 원본 필드 | 나온 비율 | 예시 값 |\n| --- | --- | --- |\n" % (g, n))
        for k, c in fields[g].most_common():
            o.write("| %s | %d%% | %s |\n" % (k, 100 * c // n, ex[g].get(k, "").replace("|", "/")))
        o.write("\n")
    o.write("## 첫 3줄 원문\n\n```\n" + "\n".join(x[:400] for x in lines[:3]) + "\n```\n")
print("형식:", fmt, "/ 종류:", dict(cnt.most_common()))
