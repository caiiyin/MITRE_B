import gzip, json, sys
from collections import defaultdict, Counter
path, out = sys.argv[1], sys.argv[2]
key = sys.argv[3] if len(sys.argv) > 3 else None
MAX_LINES, PER_GROUP = 500000, 500
def flat(d, pre=""):
    for k, v in d.items():
        if isinstance(v, dict):
            yield from flat(v, pre + k + ".")
        else:
            yield pre + k, v
cnt = Counter(); fields = defaultdict(Counter); ex = defaultdict(dict); raws = defaultdict(list)
with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
    for i, line in enumerate(f, 1):
        if i > MAX_LINES: break
        try: r = json.loads(line).get("result", {})
        except Exception: continue
        raw = r.get("_raw", "")
        try: rj = json.loads(raw) if raw.startswith("{") else None
        except Exception: rj = None
        g = (rj or {}).get(key) if key else "all"
        g = g or r.get(key, "-") if key else g
        cnt[g] += 1
        if cnt[g] > PER_GROUP: continue
        if rj:
            for k, v in flat(rj):
                fields[g][k] += 1
                if k not in ex[g] and v not in ("", None): ex[g][k] = str(v)[:60]
        elif len(raws[g]) < 3:
            raws[g].append(raw[:300])
with open(out, "w", encoding="utf-8") as o:
    o.write("# 필드 목록: %s\n\n앞 %d줄 기준, 종류별 최대 %d건 표본\n\n" % (path.split("\\")[-1], MAX_LINES, PER_GROUP))
    for g, n in cnt.most_common():
        o.write("## %s (%d건)\n\n" % (g, n))
        if fields[g]:
            s = min(n, PER_GROUP)
            o.write("| 원본 필드 | 나온 비율 | 예시 값 |\n| --- | --- | --- |\n")
            for k, c in sorted(fields[g].items()):
                o.write("| %s | %d%% | %s |\n" % (k, 100 * c // s, ex[g].get(k, "").replace("|", "/")))
        for r0 in raws[g]:
            o.write("\n```\n%s\n```\n" % r0)
        o.write("\n")
print("종류:", dict(cnt.most_common()))
print("저장:", out)
