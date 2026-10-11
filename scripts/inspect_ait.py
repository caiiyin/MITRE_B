import re, sys, os, glob
from collections import Counter, defaultdict
root, out = sys.argv[1], sys.argv[2]
host = "intranet_server"
g = os.path.join(root, "gather", host, "logs")
def lines(p, n=None):
    with open(p, encoding="utf-8", errors="ignore", newline="") as f:
        for i, l in enumerate(f.read().split("\n"), 1):
            if n and i > n: break
            yield i, l.rstrip("\r")
o = open(out, "w", encoding="utf-8")
w = lambda s="": o.write(s + "\n")
w("# AIT russellmitchell 필드 목록 (%s)\n" % host)
y = os.path.join(root, "dataset.yaml")
if os.path.exists(y):
    w("## dataset.yaml\n```\n" + open(y, encoding="utf-8", errors="ignore").read()[:1500] + "\n```\n")
w("## 파일 목록\n")
for p in sorted(glob.glob(os.path.join(g, "**", "*"), recursive=True)):
    if os.path.isfile(p):
        w("- %s (%d KB)" % (os.path.relpath(p, root), os.path.getsize(p) // 1024))
# auth.log
p = os.path.join(g, "auth.log")
prog, ex = Counter(), {}
first = last = None; n = 0
for i, l in lines(p):
    m = re.match(r"^(\w{3} [ \d]\d \d\d:\d\d:\d\d) (\S+) ([^\[:\s]+)", l)
    if not m: continue
    n += 1; first = first or m.group(1); last = m.group(1)
    prog[m.group(3)] += 1
    ex.setdefault(m.group(3), l[:200])
w("\n## auth.log (%d줄, %s ~ %s)\n\n| 프로그램 | 줄 수 | 예시 |\n| --- | --- | --- |" % (n, first, last))
for k, c in prog.most_common(12):
    w("| %s | %d | `%s` |" % (k, c, ex[k].replace("|", "/")))
# audit.log
p = os.path.join(g, "audit", "audit.log")
typ, keys, ex = Counter(), defaultdict(Counter), {}
ts = []
for i, l in lines(p, 300000):
    m = re.match(r"type=(\S+) msg=audit\((\d+\.\d+):\d+\):(.*)", l)
    if not m: continue
    t = m.group(1); typ[t] += 1; ts.append(float(m.group(2)))
    for k in re.findall(r"(\w+)=", m.group(3)): keys[t][k] += 1
    ex.setdefault(t, l[:220])
w("\n## audit.log (앞 300000줄, epoch %s ~ %s)\n" % (min(ts) if ts else "-", max(ts) if ts else "-"))
for t, c in typ.most_common(12):
    w("### %s (%d줄)\n\n키: %s\n\n`%s`\n" % (t, c, ", ".join(k for k, _ in keys[t].most_common(30)), ex[t].replace("`", "'")))
# apache
w("\n## apache2 (각 파일 앞 3줄)\n")
for p in sorted(glob.glob(os.path.join(g, "apache2", "*")))[:15]:
    w("### %s\n```" % os.path.basename(p))
    for i, l in lines(p, 3): w(l[:300])
    w("```")
# labels
w("\n## labels (각 파일 앞 3줄)\n")
for p in sorted(glob.glob(os.path.join(root, "labels", "**", "*"), recursive=True)):
    if os.path.isfile(p):
        w("### %s\n```" % os.path.relpath(p, root))
        for i, l in lines(p, 3): w(l[:300])
        w("```")
o.close(); print("저장:", out)
