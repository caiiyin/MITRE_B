import gzip, json, re, os, glob, sys
from collections import Counter
D = sys.argv[1]; N = 200000
EMPTY = {"-", "?", "(none)", "(null)", "NULL SID", ""}
def report(name, rows, fields):
    rows = list(rows); n = len(rows) or 1
    print("\n== %s (%d줄 표본)" % (name, len(rows)))
    for f in fields:
        vals = [r.get(f) for r in rows]
        empty = Counter(v for v in vals if v is None or v in EMPTY)
        print("  %-22s 채워짐 %5.1f%%   빈 값: %s" % (f, 100 * (n - sum(empty.values())) / n, dict(empty.most_common(3))))
def lines(p, gz=False):
    f = gzip.open(p, "rt", encoding="utf-8", errors="ignore") if gz else open(p, encoding="utf-8", errors="ignore")
    for i, l in enumerate(f):
        if i >= N: break
        yield l.rstrip("\r\n")
# LANL
def lanl(name, cols):
    for l in lines(os.path.join(D, "lanl", name), True):
        yield dict(zip(cols, l.split(",")))
report("LANL auth", lanl("auth_window.txt.gz", ["t","src_user","dst_user","src_host","dst_host","auth_type","logon_type","orient","status"]), ["src_user","dst_user","src_host","dst_host","auth_type","logon_type"])
report("LANL proc", lanl("proc_window.txt.gz", ["t","user","host","proc","act"]), ["user","host","proc"])
report("LANL dns", lanl("dns_window.txt.gz", ["t","src_host","query"]), ["src_host","query"])
# AIT
A = os.path.join(D, "ait_lds", "russellmitchell", "gather")
def authlog():
    for p in glob.glob(os.path.join(A, "*", "logs", "auth.log*")):
        for l in lines(p):
            m = re.match(r"^\w{3} [ \d]\d [\d:]{8} (\S+) ([^\[:\s]+)(?:\[\d+\])?: (.*)", l)
            if not m: continue
            host, prog, msg = m.groups(); r = {"host": host, "prog": prog}
            if prog == "sudo":
                s = re.match(r"\s*(\S+) : .*?USER=(\S+) ; COMMAND=(.*)", msg)
                if s: r.update(actor=s.group(1), target=s.group(2), cmd=s.group(3))
                yield r
            elif prog in ("su", "sshd"):
                s = re.search(r"(?:for|user) (\S+)", msg); r["user"] = s.group(1) if s else None
                s = re.search(r"from (\S+)", msg); r["src_ip"] = s.group(1) if s else None
                yield r
report("AIT auth.log sudo", (r for r in authlog() if r["prog"] == "sudo"), ["host","actor","target","cmd"])
report("AIT auth.log su/sshd", (r for r in authlog() if r["prog"] != "sudo"), ["host","user","src_ip"])
def audit():
    for p in glob.glob(os.path.join(A, "*", "logs", "audit", "audit.log")):
        for l in lines(p):
            if re.match(r"type=(USER_LOGIN|USER_AUTH|USER_CMD|EXECVE|SYSCALL) ", l):
                yield {k: v.strip('"') for k, v in re.findall(r"(\w+)=(\"[^\"]*\"|\S+)", l)}
report("AIT auditd (사용 type만)", audit(), ["type","auid","uid","acct","exe","hostname","addr","terminal","tty"])
def apache():
    pat = re.compile(r'^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\S+) (\S+) "([^"]*)" "([^"]*)"')
    for p in glob.glob(os.path.join(A, "*", "logs", "apache2", "*-access.log*")):
        for l in lines(p):
            m = pat.match(l)
            if m: yield dict(zip(["ip","ident","user","time","req","status","bytes","referer","ua"], m.groups()))
report("AIT Apache access", apache(), ["ip","user","req","status","bytes","referer","ua"])
# Zeek
def zeek():
    for l in lines(os.path.join(D, "apt29", "combined_zeek.log")):
        try: d = json.loads(l)
        except Exception: continue
        if d.get("@stream") in ("conn","http","dns","kerberos","smb_files","smb_mapping","ssl"):
            yield {"stream": d["@stream"], "orig_h": d.get("id_orig_h"), "resp_h": d.get("id_resp_h"), "client": d.get("client") if d["@stream"]=="kerberos" else "n/a"}
report("Zeek (사용 stream)", zeek(), ["orig_h","resp_h"])
report("Zeek kerberos", (r for r in zeek() if r["stream"] == "kerberos"), ["client"])
