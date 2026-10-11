# MITRE ATT&CK 기반 다중 플랫폼 위협 탐지 엔진 — 트랙 B

이기종 보안 로그를 OCSF 공통 스키마로 정규화하고, 한 환경 안에서 벌어진 다단계 공격을 **공격 흐름**으로 재구성하는 탐지 엔진을 만든다. 이 저장소의 트랙 B는 다단계 공격 흐름 탐지(연관분석)를 맡는다.

- 트랙 A: ATT&CK Technique별 탐지 룰 (Splunk attack_data, Sigma-AWS)
- 트랙 B: 공격 흐름 연관분석 (BOTS v1, OTRF APT29, LANL, AIT-LDS v2)

## 진행 상황

| 주차 | 내용 | 상태 |
| --- | --- | --- |
| 1주차 | 데이터 확보, 필요한 구간만 잘라 보관, 이벤트 수 집계 | 완료 |
| 2주차 | 데이터셋별 정답 타임라인 작성, 트랙 A에 기법 목록 전달 | 진행 중 (APT29 Day1 단계별 시각 찾는 중) |

## 실행 환경

- Windows 10/11, PowerShell
- Python 3.10 이상 (`python --version`으로 확인)
- 추가 패키지: `openpyxl` (2주차 APT29 계획 읽기용)

```powershell
python -m pip install openpyxl
```

모든 명령은 프로젝트 폴더를 `C:\dev\Mitre`로 두는 기준이다.

## 폴더 구조

```
C:\dev\Mitre\
├── data\                  원본 데이터 (GitHub에 올리지 않음, .gitignore)
│   ├── bots_v1\
│   ├── apt29\
│   ├── lanl\
│   └── ait_lds\russellmitchell\
├── labels\                데이터셋별 정답 타임라인 CSV
├── scripts\
│   ├── data_tools.py      1주차: 다운로드·자르기·집계 도구
│   └── week2_tools.py     2주차: 정답 타임라인 작성 도구
└── docs\
    ├── data_inventory.csv         데이터셋별 원본·보관 이벤트 수
    ├── data_cut_log.md            무엇을 어떤 기준으로 보관·제외했는지
    ├── ait_keep_list.txt          AIT-LDS에서 꺼낸 63개 파일 목록
    ├── mapping_ait_russellmitchell.csv   AIT 서버·IP·사용자 대응표
    └── week2\                     2주차 결과 (레드팀 요약, 기법 목록 등)
```

원본 데이터는 용량이 커서 저장소에 포함하지 않는다. 아래 "데이터 받기"의 명령으로 같은 결과를 다시 만들 수 있다.

## 데이터 요약

| 데이터셋 | 로그 소스 | 원본 이벤트 수 | 보관 이벤트 수 | 보관 기준 |
| --- | --- | ---: | ---: | --- |
| BOTS v1 | iis | 22,615 | 22,615 | sourcetype 선택 |
| BOTS v1 | suricata | 3,563,643 | 3,563,643 | sourcetype 선택 |
| BOTS v1 | WinEventLog:Security | 14,218,920 | 14,218,920 | sourcetype 선택 |
| BOTS v1 | Sysmon | 830,389 | 830,389 | sourcetype 선택 |
| APT29 | Day1 호스트 로그 | 196,081 | 196,081 | Day1만, 압축 상태 |
| APT29 | Day1 Zeek | 2,140 | 2,140 | Day1만 |
| LANL | auth | 1,051,430,459 | 507,202,666 | 레드팀 기간 ±1일 |
| LANL | proc | 426,045,096 | 203,276,844 | 레드팀 기간 ±1일 |
| LANL | dns | 40,821,591 | 6,072,630 | 레드팀 기간 ±1일 |
| LANL | redteam | 749 | 749 | 전체 |
| AIT-LDS v2 | russellmitchell | 미집계 | 63개 파일 | 라벨 있는 서버 4곳의 텍스트 로그 |

자세한 보관·제외 기준과 파일 구조는 `docs/data_cut_log.md`에 있다.

## 데이터 받기

원본을 통째로 보관하지 않고, **받으면서 필요한 부분만 자르고 원본은 지우는** 방식으로 디스크 사용량을 줄였다. 원본을 지우기 전에는 항상 `peek`로 처음·끝 줄을 확인한다.

### 1. Splunk BOTS v1

출처: https://github.com/splunk/botsv1 (README의 "JSON - by Sourcetype")

Splunk 없이 sourcetype별 JSON 압축 파일을 직접 받는다.

```powershell
cd C:\dev\Mitre\data\bots_v1
curl.exe -O https://s3.amazonaws.com/botsdataset/botsv1/json-by-sourcetype/botsv1.iis.json.gz
curl.exe -O https://s3.amazonaws.com/botsdataset/botsv1/json-by-sourcetype/botsv1.suricata.json.gz
curl.exe -O https://s3.amazonaws.com/botsdataset/botsv1/json-by-sourcetype/botsv1.WinEventLog-Security.json.gz
curl.exe -O https://s3.amazonaws.com/botsdataset/botsv1/json-by-sourcetype/botsv1.XmlWinEventLog-Microsoft-Windows-Sysmon-Operational.json.gz
cd C:\dev\Mitre
```

이벤트 수 세기 (iis·Security·Sysmon은 마지막 `lastrow` 표시 줄 1개를 뺀다):

```powershell
python C:\dev\Mitre\scripts\data_tools.py count-file C:\dev\Mitre\data\bots_v1\botsv1.iis.json.gz
```

### 2. OTRF APT29 Evals

출처: https://github.com/OTRF/detection-hackathon-apt29

저장소는 Git LFS를 쓰지 않으므로 필요한 파일만 직접 받는다.

```powershell
cd C:\dev\Mitre\data\apt29
curl.exe -L -O https://raw.githubusercontent.com/OTRF/detection-hackathon-apt29/master/datasets/day1/apt29_evals_day1_manual.zip
curl.exe -L -O https://raw.githubusercontent.com/OTRF/detection-hackathon-apt29/master/datasets/day1/zeek/combined_zeek.log
curl.exe -L -O https://raw.githubusercontent.com/OTRF/detection-hackathon-apt29/master/emulation-plans/apt29.xlsx
cd C:\dev\Mitre
```

호스트 로그 zip은 풀지 않고(풀면 385MB) 그대로 읽는다.

```powershell
python C:\dev\Mitre\scripts\data_tools.py zip-count C:\dev\Mitre\data\apt29\apt29_evals_day1_manual.zip
```

Day2는 7주차에 받는다. Day2 Zeek 파일은 Day1과 이름이 같으므로 `combined_zeek_day2.log`로 저장한다.

### 3. LANL Comprehensive Cyber-Security Events

출처: https://csr.lanl.gov/data/cyber1/ (이메일과 사용 목적을 입력해야 받을 수 있음)

`redteam.txt.gz`로 레드팀 활동 기간을 구하고, 그 앞뒤 하루씩만 남긴다.

```powershell
python C:\dev\Mitre\scripts\data_tools.py lanl-window C:\dev\Mitre\data\lanl\redteam.txt.gz
```

결과: `--start 64485 --end 2643447`. 파일을 하나씩 받아 자르고, 확인한 뒤 원본을 지운다.

```powershell
python C:\dev\Mitre\scripts\data_tools.py lanl-cut C:\dev\Mitre\data\lanl\auth.txt.gz C:\dev\Mitre\data\lanl\auth_window.txt.gz --start 64485 --end 2643447
python C:\dev\Mitre\scripts\data_tools.py peek C:\dev\Mitre\data\lanl\auth_window.txt.gz
Remove-Item C:\dev\Mitre\data\lanl\auth.txt.gz
```

`proc.txt.gz`, `dns.txt.gz`도 같은 방법으로 처리한다. `flows`는 받지 않는다.

### 4. AIT Log Data Set V2.0 (russellmitchell)

출처: https://zenodo.org/records/5789064

zip(7.1GB)을 받지 않고, 서버에서 목록에 적은 63개 파일만 꺼낸다.

```powershell
python C:\dev\Mitre\scripts\data_tools.py zip-list "https://zenodo.org/records/5789064/files/russellmitchell.zip?download=1" --summary
python C:\dev\Mitre\scripts\data_tools.py zip-extract "https://zenodo.org/records/5789064/files/russellmitchell.zip?download=1" C:\dev\Mitre\data\ait_lds\russellmitchell --list C:\dev\Mitre\docs\ait_keep_list.txt
```

한국어 Windows에서 결과를 파일로 저장할 때는 먼저 `$env:PYTHONIOENCODING = "utf-8"`을 실행한다.

## 도구 사용법

### data_tools.py (1주차)

| 명령 | 하는 일 |
| --- | --- |
| `lanl-window <redteam.txt.gz>` | 레드팀 활동 기간과 자를 구간 계산 |
| `lanl-cut <원본> <결과> --start S --end E` | 시간 구간만 남겨 새 .gz로 저장 (`--fast`: 구간 끝에서 멈춤) |
| `count-file <파일>` | 줄 수 세기, 압축 손상 확인 겸용 |
| `count-url <주소>` | 저장하지 않고 원격 파일 줄 수 세기 |
| `peek <파일> [--lines N]` | 처음과 마지막 몇 줄 보기 |
| `zip-list <zip 또는 주소> [--summary]` | zip 안의 파일 목록과 크기 |
| `zip-extract <zip 또는 주소> <폴더> --list <목록>` | 목록의 파일만 꺼내기 |
| `zip-count <zip 또는 주소>` | zip 안 파일들의 줄 수 (풀지 않음) |

zip 자리에 `https://` 주소를 넣으면 전체를 받지 않고 필요한 부분만 서버에서 읽는다(서버가 부분 읽기를 지원해야 함).

### week2_tools.py (2주차)

| 명령 | 하는 일 |
| --- | --- |
| `redteam-summary <redteam.txt.gz> --out <csv>` | LANL 레드팀 계정·기간 요약 |
| `grep <파일> <검색어...> [--all] [--max N]` | 검색어가 든 이벤트의 시각·호스트와 가장 이른·늦은 시각 |
| `apt29-steps <apt29.xlsx> --day day1 --out <csv>` | APT29 계획을 정답 타임라인 양식으로 내보내기 |
| `fill-ids <타임라인.csv>` | 예전 ATT&CK 이름을 보고 technique_id 자동 채우기 |
| `timeline-template <csv> --dataset <이름> --scenario <이름>` | 빈 정답 타임라인 양식 만들기 |

## 정답 타임라인 (labels 폴더)

모든 타임라인은 같은 열을 쓴다.

```
dataset_id, scenario_id, stage_no, step, tactic, technique_id, technique_name,
start_utc, end_utc, actor_user, actor_ip, host, evidence_source, evidence_query, notes
```

| 파일 | 시나리오 | 근거 자료 |
| --- | --- | --- |
| `apt29_day1_timeline.csv` | APT29 Day1 (25단계) | 에뮬레이션 계획 `apt29.xlsx` |
| `bots_v1_web_defacement_timeline.csv` | 웹사이트 변조 | Splunk 공식 BOTS v1 문제·정답 |
| `bots_v1_cerber_timeline.csv` | Cerber 랜섬웨어 | Splunk 공식 BOTS v1 문제·정답 |
| `lanl_redteam_timeline.csv` | 레드팀 탈취 계정 상위 10개 | `redteam.txt` |
| `ait_russellmitchell_timeline.csv` | VPN 침투 → 웹셸 → 권한 상승, DNS 유출(별도 시나리오) | `attacks.log`, `dnsteal.log`, `openvpn.log` |

데이터셋별 기법을 모은 `docs/week2/trackB_techniques.csv`를 트랙 A에 전달했다.

## 데이터를 다룰 때 알아 둘 점

- **APT29의 Zeek와 호스트 로그는 서로 다른 시간에 기록되었다.** (Day1 Zeek 2020-04-30, 호스트 2020-05-02) 그래서 APT29는 호스트 로그 안에서만 연관분석하고, 호스트-네트워크 연관분석은 BOTS v1과 AIT-LDS로 검증한다.
- **BOTS v1 파일은 시간순이 아니다.** 파서에서 정렬해야 한다. 시각은 소스마다 기준이 다르다: iis·Security·Sysmon 원본은 UTC, `_time`은 MDT(UTC-6), Suricata는 `-0600`으로 표기되어 있으나 실제 UTC일 가능성이 있어 3주차에 확인한다.
- **AIT-LDS는 모든 서버가 UTC다.** 공격자는 원격 직원 jhall의 VPN 인증서로 접속했고(외부 IP 192.168.230.122, VPN 내부 IP 10.9.0.10), DNS 유출은 VPN 공격과 별개로 internal-share에서 일어났다. dnsmasq 로그는 연도가 없어 2022를 붙여야 한다.
- **LANL 시각은 실제 날짜가 아니라** 데이터 시작부터 센 초다.

## 참고 자료

- Splunk, [BOTS v1](https://github.com/splunk/botsv1), [BOTS 문제·정답 공개 안내](https://www.splunk.com/en_us/blog/security/boss-of-the-soc-scoring-server-questions-and-answers-and-dataset-open-sourced-and-ready-for-download.html)
- OTRF, [APT29 Evals Detection Hackathon](https://github.com/OTRF/detection-hackathon-apt29)
- Los Alamos National Laboratory, [Comprehensive, Multi-Source Cyber-Security Events](https://csr.lanl.gov/data/cyber1/)
- AIT, [AIT Log Data Set V2.0](https://zenodo.org/records/5789064)
- [MITRE ATT&CK](https://attack.mitre.org), [OCSF Schema](https://schema.ocsf.io/)
