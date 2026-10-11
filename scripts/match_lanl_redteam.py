import gzip, sys, csv
d, out = sys.argv[1], sys.argv[2]
rt = {}
with gzip.open(d + "\\redteam.txt.gz", "rt", encoding="utf-8") as f:
    for l in f:
        p = l.strip().split(",")
        if len(p) == 4:
            rt.setdefault((int(p[0]), p[1].lower(), p[2].lower(), p[3].lower()), []).append(p)
times = {k[0] for k in rt}
found = {k: [] for k in rt}
n = last = 0
with gzip.open(d + "\\auth_window.txt.gz", "rt", encoding="utf-8", errors="ignore", newline="") as f:
    for line in f:
        n += 1
        if n % 100000000 == 0: print("  ", n // 1000000, "백만 줄 ...", flush=True)
        c = line.rstrip("\r\n").split(",")
        t = int(c[0]); last = t
        if t not in times or len(c) != 9: continue
        su, du, sc, dc = c[1].lower(), c[2].lower(), c[3].lower(), c[4].lower()
        for which, u in (("src_user", su), ("dst_user", du)):
            k = (t, u, sc, dc)
            if k in found:
                found[k].append((n, which, c[5], c[6], c[7], c[8]))
first = 64485
inside = [k for k in rt if first <= k[0] <= last]
hit = [k for k in inside if found[k]]
with open(out, "w", newline="", encoding="utf-8") as o:
    w = csv.writer(o)
    w.writerow(["rt_time", "user", "src_computer", "dst_computer", "raw_ref", "match_on", "auth_type", "logon_type", "orientation", "status"])
    for k in sorted(rt):
        for (ln, which, a, lt, ori, st) in found[k] or [("", "", "", "", "", "")]:
            w.writerow([k[0], rt[k][0][1], rt[k][0][2], rt[k][0][3], ("lanl/auth_window.txt.gz:%s" % ln) if ln else "", which, a, lt, ori, st])
print("auth 줄 수:", n, "/ 시각 범위:", first, "~", last)
print("redteam 전체:", len(rt), "/ 구간 안:", len(inside), "/ 일치:", len(hit), "/ 구간 안인데 불일치:", len(inside) - len(hit))
print("일치한 auth 줄 수:", sum(len(found[k]) for k in hit))
print("저장:", out)
