import gzip, re, sys
path, start, end, words = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
def get(k, line):
    m = re.search(r'"%s"\s*:\s*"([^"]+)"' % re.escape(k), line)
    return m.group(1) if m else "-"
rows = []
with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if all(w in line for w in words):
            t = get("_time", line)
            if start <= t[:19] <= end:
                rows.append((t[:23], get("event_type", line), get("http.http_method", line), get("src_ip", line), get("dest_ip", line)))
for r in sorted(rows):
    print("  ".join(r))
print("총", len(rows), "건")
