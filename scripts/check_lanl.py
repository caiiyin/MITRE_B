import gzip, sys
from collections import Counter
d = sys.argv[1]
for name in ["auth_window", "proc_window", "dns_window"]:
    with gzip.open(d + "\\" + name + ".txt.gz", "rt", encoding="utf-8", errors="ignore") as f:
        head = [next(f).rstrip("\n") for _ in range(1000)]
    print("==", name, "열 수:", dict(Counter(len(l.split(",")) for l in head)), "첫 시각:", head[0].split(",")[0])
    for l in head[:3]: print("   ", l)
with gzip.open(d + "\\redteam.txt.gz", "rt", encoding="utf-8") as f:
    rt = [l.rstrip("\n").split(",") for l in f if l.strip()]
t = [int(r[0]) for r in rt]
print("== redteam", len(rt), "줄, 시각", min(t), "~", max(t), "/ 사용자", len({r[1] for r in rt}), "명")
for r in rt[:3]: print("   ", ",".join(r))
