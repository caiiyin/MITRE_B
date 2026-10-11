## OTRF APT29 Evals
- 출처: https://github.com/OTRF/detection-hackathon-apt29
- 받은 파일 (C:\dev\Mitre\data\apt29\)
  - apt29_evals_day1_manual.zip: Day1 호스트 로그 (Sysmon, Windows 보안 로그, PowerShell 로그 등). 압축을 풀지 않고 보관 (풀면 385MB)
  - combined_zeek.log: Day1 네트워크 로그 (Zeek)
  - apt29.xlsx: 에뮬레이션 계획 (2주차 정답 타임라인의 기준)
- 받는 방법: git clone 없이 curl.exe로 위 3개 파일만 받음
- 제외: Day1·Day2 PCAP (Zeek 로그가 PCAP을 분석한 결과라 불필요), Day2 전체 (7주차에 같은 방법으로 받을 예정)
- 이벤트 수: 호스트 로그 196,081건, Zeek 2,140건

### Zeek 로그 주요 필드
- ts: 시간 (유닉스 시간, 초 단위)
- id_orig_h: 출발지 IP
- id_resp_h: 목적지 IP
- id_resp_p: 목적지 포트
- @stream: 로그 종류 (conn, dns 등)

### APT29 주의: 네트워크와 호스트 로그 시간 불일치
- Day1 Zeek: 2020-04-30 00:06~00:45 UTC / Day1 호스트: 2020-05-02 02:55~03:28 UTC
- Day2 Zeek: 2020-05-01 07:02~05-02 02:16 UTC / Day2 호스트: 2020-05-02 07:54~08:29 UTC
- 같은 공격 실행의 기록이 아니므로 APT29에서는 호스트-네트워크 연관분석을 하지 않음
- APT29는 호스트 로그 내부(Sysmon, Security, PowerShell) 연관분석에만 사용
- 호스트-네트워크 연관분석 검증은 BOTS v1과 AIT-LDS로 수행
- 참고: Day2 호스트 로그는 587,286줄 (7주차 집계용)

## AIT-LDS v2 (russellmitchell)
- 출처: https://zenodo.org/records/5789064
- 원본: zip 7.1GB, 전체 해제 시 14.98GB, 파일 14,911개
- 받는 방법: zip을 받지 않고, data_tools.py zip-extract --list로 서버에서 목록의 파일만 꺼냄
- 목록: docs/ait_keep_list.txt (63개 파일)
- 보관: 라벨이 있는 서버 4곳(intranet_server, internal_share, vpn, inet-firewall)의 텍스트 로그, 정답 라벨, 공격자 시간표(attacks.log 등), servers.yaml, dataset.yaml
- 제외: log.pcap.* 원본 패킷(약 6GB, 이름이 .pcap으로 끝나지 않음에 주의), suricata stats.log(약 1GB)·eve.json(약 1.4GB), journal 바이너리, 공격자 traffic.pcap·traffic.json·탈취 파일
- 보관 용량: (확인 필요) MB
- 공격 시각: 2022-01-24 03:01 ~ 04:39 (Zenodo 설명 기준)

## Splunk BOTS v1
- 출처: https://github.com/splunk/botsv1 (JSON - by Sourcetype)
- 받는 방법: Splunk 없이 sourcetype별 JSON 압축 파일을 curl.exe로 직접 받음
- 보관 (C:\dev\Mitre\data\bots_v1\, 압축 상태 그대로)
  - botsv1.iis.json.gz: 22,615건
  - botsv1.suricata.json.gz: 3,563,643건
  - botsv1.WinEventLog-Security.json.gz: 14,218,920건
  - botsv1.XmlWinEventLog-Microsoft-Windows-Sysmon-Operational.json.gz: 830,389건
- 제외: 전체 JSON(압축 11.3GB, 해제 시 약 120GB), stream 계열 등 나머지 sourcetype
- 다음 작업: 2주차에 공개 풀이로 공격 시간대를 확인한 뒤, 3주차에 공격 구간 앞뒤만 남기고 정리

### BOTS v1 파일 구조 (iis 기준)
- 한 줄 = {"preview", "offset", "result": {이벤트}}. 이벤트 내용은 result 안에 있음
- 마지막 줄 {"preview":false,"lastrow":true}는 내보내기 끝 표시라 이벤트 아님 → 이벤트 수 = 줄 수 - 1
- 시간순 정렬 아님 (첫 줄 8/24, 마지막 이벤트 8/10). 연관분석 전에 정렬 필요, 자를 때 --fast 사용 불가
- 시간: _raw 안의 시각은 UTC, _time은 MDT(UTC-6). 모두 UTC로 통일할 것
- 원본 로그: result._raw → 파서 입력으로 사용
- Splunk가 뽑아 둔 필드(c_ip, s_ip, cs_method, cs_uri_stem, sc_status 등)는 파서 결과 검증용으로만 사용
- 사용 안 함: _bkt, _cd, _serial, _si, splunk_server, _indextime, _kv

### BOTS v1 파일별 구조
- iis: _raw = 공백 구분 텍스트, 시간 UTC, lastrow 표시 줄 있음 → 22,615건
- WinEventLog:Security: _raw = key=value 줄 + Message 본문, 첫 줄 "MM/DD/YYYY HH:MM:SS PM" 형식(24시간제, AM/PM 무시), UTC, lastrow 있음 → 14,218,920건
  - Account Name 등은 Subject와 Target에 두 번 나옴
- Sysmon: _raw = XML, EventData의 UtcTime이 UTC, lastrow 있음 → 830,389건
- suricata: _raw = EVE JSON, timestamp에 -0600 표기(실제 UTC일 가능성, 3주차에 Sysmon과 비교해 확인), lastrow 없음 → 3,563,643건
- 확인 필요: 192.168.250.70이 iis에서는 we1149srv, Sysmon에서는 we5201srv로 나옴

### AIT-LDS russellmitchell 환경 정보 (servers.yaml)
- 모든 서버의 timezone이 UTC → 로그 시각은 변환 없이 UTC로 사용
- 공격자: attacker-0, 192.168.230.122 (외부)
- 공격자는 VPN(172.19.131.174)으로 접속 → 내부 서버 로그에는 VPN이 나눠 준 내부 IP로 기록됨 (openvpn.log로 확인)
- 웹셸 대상: intranet-server 10.143.2.4
- 방화벽 겸 DNS: inet-firewall (172.19.128.1, 192.168.230.4, 10.143.0.1)
- 원격 직원 3명(ahayes, twhite, jhall)도 VPN을 정상적으로 사용 → VPN 접속만으로는 공격 판단 불가 (오탐 비교 대상)
- 서버-IP-사용자 대응표: docs/mapping_ait_russellmitchell.csv
- 공격자는 원격 직원 jhall의 VPN 인증서로 접속함 (진짜 jhall: 192.168.230.165, 공격자: 192.168.230.122). 같은 사용자의 처음 보는 접속 IP → 행위 특징 "새로운 호스트 접속"의 검증 사례

### AIT-LDS russellmitchell 정답 타임라인 확인 결과
- 공격자 VPN 내부 IP: 10.9.0.10 (openvpn.log의 "pool returned", "Learn" 줄). VPN 안의 공격은 내부 로그에 이 IP로 남음
- VPN 세션: 2022-01-24 03:01:00 ~ 04:42:05 UTC (attacks.log의 vpn_disconnect는 04:38:11, VPN 서버 기록은 약 4분 늦음)
- DNS 유출은 별도 사건: internal-share(10.143.0.103)에서 2022-01-20 12:48:27 ~ 01-24 13:50:03 UTC
  - 도메인 email-19.kennedy-mendoza.info, 공격자 수신 19,954회, 파일 32개
  - 피해 쪽 dnsmasq.log에 53,054줄 (1월 21일 0시부터. 1월 20일분은 받지 않은 이전 파일에 있음)
  - 타임라인에서는 scenario_id를 russellmitchell_dns_exfil로 분리
- 파서 주의: dnsmasq.log는 "Jan 21 00:00:09" 형식으로 연도가 없음 → 2022를 붙여야 함

## LANL Comprehensive Cyber-Security Events
- 출처: https://csr.lanl.gov/data/cyber1/ (이메일과 사용 목적 입력 후 다운로드)
- 자른 기준: redteam.txt의 레드팀 활동 기간 ±1일(86400초) → --start 64485 --end 2643447
- 방법: 원본을 하나씩 받아 data_tools.py lanl-cut으로 자르고, peek로 처음·끝 시각을 확인한 뒤 원본 삭제
- auth: 원본 1,051,430,459건 → 보관 507,202,666건 (약 48%), 3,465.1MB, 처리 3,109초
- proc: 원본 426,045,096건 → 보관 203,276,844건 (약 48%), 1,082.6MB
- dns: 원본 40,821,591건 → 보관 6,072,630건 (약 15%), 26.2MB, 처리 40초
- redteam: 749줄, 전체 보관
- 제외: flows (가장 큰 파일, 연관분석에는 auth·proc이 핵심이라 제외)
- 시각은 실제 날짜가 아니라 데이터 시작부터 센 초 (개인정보 보호를 위해 LANL이 날짜를 숨김)
- 형식
  - auth: 시각,출발 사용자,도착 사용자,출발 컴퓨터,도착 컴퓨터,인증 방식,로그온 종류,방향,결과
  - proc: 시각,사용자@컴퓨터,컴퓨터,프로세스,Start/End
  - dns: 시각,요청한 컴퓨터,찾은 컴퓨터
- 참고: dns는 보관 비율(약 15%)이 auth(약 48%)보다 훨씬 낮음. dns 기록이 레드팀 기간 밖에 더 많이 몰려 있다는 뜻