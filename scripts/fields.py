import gzip, re, sys
from collections import Counter
path, words = sys.argv[1], sys.argv[2:]
keys = ["Image", "ParentImage", "CommandLine", "Computer", "User"]
found = {k: Counter() for k in keys}
tpat = re.compile(r'"_time"\s*:\s*"([^"]+)"')
times = []
with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if not all(w in line for w in words):
            continue
        m = tpat.search(line)
        if m: times.append(m.group(1))
        for k in keys:
            for p in (r"Name='%s'>([^<]+)<" % k, r"<%s>([^<]+)</%s>" % (k, k), r'"%s"\s*:\s*"([^"]+)"' % k):
                for v in re.findall(p, line):
                    found[k][v] += 1
print("건수:", len(times))
if times:
    print("시작:", min(times))
    print("끝  :", max(times))
for k in keys:
    print("\n[%s]" % k)
    for v, c in found[k].most_common(5):
        print("  %5d  %s" % (c, v))
