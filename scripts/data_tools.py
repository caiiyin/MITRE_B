"""
트랙 B 1주차 데이터 도구 (Windows / macOS / Linux 공통, 표준 라이브러리만 사용)

사용법 (PowerShell 또는 명령 프롬프트에서):
  python data_tools.py lanl-window  redteam.txt.gz [--margin 86400]
  python data_tools.py lanl-cut     auth.txt.gz auth_window.txt.gz --start S --end E
  python data_tools.py count-url    <다운로드 주소>
  python data_tools.py count-file   <파일.gz 또는 일반 텍스트 파일>
  python data_tools.py peek         <파일> [--lines 3]
  python data_tools.py zip-list     <파일.zip 또는 주소> [--summary]
  python data_tools.py zip-extract  <파일.zip 또는 주소> <풀 폴더> --keep gather labels --skip-ext .pcap
  python data_tools.py zip-count    <파일.zip 또는 주소>
  (zip 자리에 https:// 주소를 넣으면 전체를 받지 않고 필요한 부분만 서버에서 읽는다)
"""
import argparse
import gzip
import io

import sys
import time
import urllib.error
import urllib.request
import zipfile
from collections import deque


def open_text(path):
    """.gz면 압축을 풀지 않고 읽고, 아니면 그대로 읽는다."""
    if str(path).endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "r", encoding="utf-8", errors="replace")


def progress(n, started):
    if n % 10_000_000 == 0:
        print(f"  ... {n:,}줄 처리 ({time.time() - started:.0f}초)", file=sys.stderr)


def lanl_window(args):
    lo = hi = None
    with open_text(args.redteam) as f:
        for line in f:
            t = int(line.split(",", 1)[0])
            lo = t if lo is None else min(lo, t)
            hi = t if hi is None else max(hi, t)
    s, e = lo - args.margin, hi + args.margin
    print(f"레드팀 기간: {lo} ~ {hi}")
    print(f"자를 구간(±{args.margin}초): --start {max(s, 1)} --end {e}")


def lanl_cut(args):
    total = kept = 0
    started = time.time()
    with open_text(args.src) as fin, gzip.open(args.dst, "wt", encoding="utf-8") as fout:
        for line in fin:
            total += 1
            progress(total, started)
            t = int(line.split(",", 1)[0])
            if args.start <= t <= args.end:
                fout.write(line)
                kept += 1
            elif args.fast and t > args.end:
                break  # 시간순 정렬이라 구간이 끝나면 멈춤 (대신 원본 전체 수는 못 셈)
    label = "원본 이벤트 수(중간에 멈춤, 전체 아님)" if args.fast else "원본 이벤트 수"
    print(f"{label}: {total:,}")
    print(f"보관 이벤트 수: {kept:,}")
    print(f"걸린 시간: {time.time() - started:.0f}초")


def count_url(args):
    started = time.time()
    n = 0
    req = urllib.request.Request(args.url, headers=UA)
    with urllib.request.urlopen(req) as resp:
        stream = gzip.GzipFile(fileobj=resp) if args.url.endswith(".gz") else resp
        for _ in stream:
            n += 1
            progress(n, started)
    print(f"이벤트(줄) 수: {n:,}  (디스크에 저장하지 않음, {time.time() - started:.0f}초)")


def count_file(args):
    started = time.time()
    n = 0
    with open_text(args.path) as f:
        for _ in f:
            n += 1
            progress(n, started)
    print(f"이벤트(줄) 수: {n:,}  (압축 정상)")


def peek(args):
    head, tail = [], deque(maxlen=args.lines)
    with open_text(args.path) as f:
        for i, line in enumerate(f):
            if i < args.lines:
                head.append(line.rstrip("\n"))
            tail.append(line.rstrip("\n"))
    print("--- 처음 ---")
    print("\n".join(head))
    print("--- 마지막 ---")
    print("\n".join(tail))


class HttpFile(io.RawIOBase):
    """서버의 파일을 필요한 부분만 Range 요청으로 읽는 파일 객체 (zip을 통째로 받지 않기 위함)."""

    def __init__(self, url, block=4 * 1024 * 1024):
        self.url, self.pos, self.block = url, 0, block
        self.cache_start, self.cache = -1, b""
        # 일부 서버(Zenodo 등)는 HEAD 요청을 막으므로, 첫 1바이트만 받는 요청으로 전체 크기를 알아낸다.
        req = urllib.request.Request(url, headers=dict(UA, Range="bytes=0-0"))
        try:
            with urllib.request.urlopen(req) as r:
                content_range = r.headers.get("Content-Range", "")
                if r.status != 206 or "/" not in content_range:
                    raise RuntimeError("서버가 부분 읽기(Range)를 지원하지 않습니다. 파일을 내려받아 쓰세요.")
                self.size = int(content_range.rsplit("/", 1)[1])
                self.url = r.geturl()  # 리다이렉트된 실제 파일 주소를 이후 요청에 사용
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"서버가 요청을 거절했습니다(HTTP {e.code}). 파일을 내려받아 쓰세요.") from None

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        self.pos = {0: offset, 1: self.pos + offset, 2: self.size + offset}[whence]
        return self.pos

    def _fetch(self, start, end):
        headers = dict(UA, Range=f"bytes={start}-{end}")
        for attempt in range(5):
            try:
                with urllib.request.urlopen(urllib.request.Request(self.url, headers=headers)) as r:
                    if r.status != 206:
                        raise RuntimeError("서버가 부분 읽기(Range)를 지원하지 않습니다. 파일을 내려받아 쓰세요.")
                    return r.read()
            except (urllib.error.URLError, ConnectionError, TimeoutError):
                if attempt == 4:
                    raise
                time.sleep(3)

    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self.pos
        n = min(n, self.size - self.pos)
        if n <= 0:
            return b""
        start, end = self.pos, self.pos + n
        if not (self.cache_start <= start and end <= self.cache_start + len(self.cache)):
            if n >= self.block:
                data = self._fetch(start, end - 1)
                self.pos = end
                return data
            self.cache_start = start
            self.cache = self._fetch(start, min(start + self.block, self.size) - 1)
        off = start - self.cache_start
        data = self.cache[off:off + n]
        self.pos += len(data)
        return data

    def readinto(self, b):
        data = self.read(len(b))
        b[:len(data)] = data
        return len(data)


UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept": "*/*"}


def open_zip(path):
    if str(path).startswith("http"):
        return zipfile.ZipFile(HttpFile(path))
    return zipfile.ZipFile(path)


def zip_list(args):
    with open_zip(args.path) as z:
        infos = z.infolist()
        total = sum(i.file_size for i in infos)
        if args.summary:
            groups = {}
            for i in infos:
                key = "/".join(i.filename.split("/")[:args.depth])
                n, s = groups.get(key, (0, 0))
                groups[key] = (n + 1, s + i.file_size)
            for key, (n, s) in sorted(groups.items(), key=lambda kv: -kv[1][1]):
                print(f"{s / 1e6:12.1f} MB  {n:6d}개  {key}")
        else:
            for i in infos:
                print(f"{i.file_size / 1e6:10.1f} MB  {i.filename}")
        print(f"파일 {len(infos)}개, 압축 해제 시 전체 크기: {total / 1e9:.2f} GB")


def zip_extract(args):
    skip = tuple(e.lower() for e in args.skip_ext)
    with open_zip(args.path) as z:
        if args.list:
            with open(args.list, encoding="utf-8-sig") as f:
                wanted = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
            names = {i.filename: i for i in z.infolist()}
            missing = [w for w in wanted if w not in names]
            for w in missing:
                print(f"zip 안에 없음(건너뜀): {w}", file=sys.stderr)
            picked = [names[w] for w in wanted if w in names]
        else:
            picked = [i for i in z.infolist()
                      if not i.is_dir()
                      and any(f"/{k}/" in f"/{i.filename}" for k in args.keep)
                      and not i.filename.lower().endswith(skip)]
        size = sum(i.file_size for i in picked)
        print(f"{len(picked)}개 파일, 압축 해제 시 {size / 1e9:.2f} GB 를 풉니다.")
        for k, i in enumerate(picked, 1):
            z.extract(i, args.out)
            if k % 50 == 0 or k == len(picked):
                print(f"  ... {k}/{len(picked)}", file=sys.stderr)
    print("완료")


def zip_count(args):
    with open_zip(args.path) as z:
        for i in z.infolist():
            if i.is_dir():
                continue
            n = 0
            with z.open(i) as f:
                for _ in f:
                    n += 1
            print(f"{n:12,}줄  {i.filename}")


def main():
    # 한국어 Windows(cp949)에서 표현할 수 없는 글자가 있어도 멈추지 않게 함
    try:
        sys.stdout.reconfigure(errors="replace")
        sys.stderr.reconfigure(errors="replace")
    except AttributeError:
        pass
    p = argparse.ArgumentParser(description="트랙 B 1주차 데이터 도구")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("lanl-window", help="redteam 파일에서 자를 구간 계산")
    a.add_argument("redteam")
    a.add_argument("--margin", type=int, default=86400)
    a.set_defaults(func=lanl_window)

    a = sub.add_parser("lanl-cut", help="LANL 파일에서 구간만 남겨 새 .gz로 저장")
    a.add_argument("src")
    a.add_argument("dst")
    a.add_argument("--start", type=int, required=True)
    a.add_argument("--end", type=int, required=True)
    a.add_argument("--fast", action="store_true", help="구간이 끝나면 멈춤(빠르지만 전체 수 미집계)")
    a.set_defaults(func=lanl_cut)

    a = sub.add_parser("count-url", help="주소의 파일을 저장하지 않고 줄 수만 세기")
    a.add_argument("url")
    a.set_defaults(func=count_url)

    a = sub.add_parser("count-file", help="파일 줄 수 세기(압축 손상 확인 겸용)")
    a.add_argument("path")
    a.set_defaults(func=count_file)

    a = sub.add_parser("peek", help="처음과 마지막 몇 줄 보기")
    a.add_argument("path")
    a.add_argument("--lines", type=int, default=3)
    a.set_defaults(func=peek)

    a = sub.add_parser("zip-list", help="zip 안의 파일 목록과 크기 보기")
    a.add_argument("path")
    a.add_argument("--summary", action="store_true", help="폴더별 합계만 보기")
    a.add_argument("--depth", type=int, default=3, help="--summary에서 묶을 폴더 깊이")
    a.set_defaults(func=zip_list)

    a = sub.add_parser("zip-extract", help="zip에서 지정한 폴더만 풀기")
    a.add_argument("path")
    a.add_argument("out")
    a.add_argument("--keep", nargs="+", default=["gather", "labels"])
    a.add_argument("--skip-ext", nargs="*", default=[], help="풀지 않을 확장자 (예: .pcap)")
    a.add_argument("--list", help="꺼낼 파일 경로를 한 줄에 하나씩 적은 텍스트 파일 (--keep 대신 사용)")
    a.set_defaults(func=zip_extract)

    a = sub.add_parser("zip-count", help="zip 안 파일들의 줄 수 세기(풀지 않음)")
    a.add_argument("path")
    a.set_defaults(func=zip_count)

    args = p.parse_args()
    try:
        args.func(args)
    except RuntimeError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()