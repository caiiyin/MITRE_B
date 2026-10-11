import gzip, re, sys
path, words = sys.argv[1], sys.argv[2:]
pat = re.compile(r'"_time"\s*:\s*"([^"]+)"')
count, times, sample = 0, [], None
with gzip.open(path, "rt", encoding="utf-8", errors="ignore") as f:
    for line in f:
        if all(w in line for w in words):
            count += 1
            m = pat.search(line)
            if m: times.append(m.group(1))
            if sample is None: sample = line[:600]
print("건수:", count)
if times:
    print("시작:", min(times))
    print("끝  :", max(times))
print("예시:", sample)
