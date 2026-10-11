# 대응표: Linux · 웹 · Suricata (팀원 2)

기준: OCSF 1.1.0, 3주차 공동 작업 기준 문서의 규칙(UTC epoch ms, 빈 값은 null, 못 옮긴 필드는 unmapped.*).
양식: 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값

## 0. 공통 (BOTS export 파일)

BOTS 파일은 Splunk export라서 한 줄이 `{"preview":..., "result":{...}}` 형태예요. 원문은 `result._raw`에 들어 있고, 나머지 `result.*`는 Splunk가 뽑은 필드예요.

| 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- |
| result._raw | (파싱 대상) | 매핑은 이것만 기준으로 함. Splunk 추출 필드(result.c_ip, result.fileinfo.filename 등)는 쓰지 않음 | — |
| result._time | 쓰지 않음 | Splunk 화면 시간대(MDT)라 사용 금지 | 2016-08-10 15:56:18.000 MDT |
| result.host | device.hostname | Splunk 메타데이터지만 원문에 장비 이름이 없어서 예외로 사용. 소문자, FQDN이면 hostname과 domain으로 나눔 | suricata-ids.waynecorpinc.local → hostname=suricata-ids, domain=waynecorpinc.local |
| (파일 경로 + 줄 번호) | raw_ref | 데이터 폴더 기준 상대 경로, 1부터, 압축 푼 기준, `\n`으로만 나눔 | bots_v1/botsv1.suricata.json.gz:3347900 |
| (상수) | dataset_id | 고정값 | bots_v1 |
| (상수) | label | 파서는 항상 null. 라벨은 별도 단계에서 raw_ref로 붙임 | null |

## 1. Suricata (`_raw` = EVE JSON)

### 1-1. 모든 event_type 공통

| 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- |
| timestamp | time | `-0600` 오프셋을 반영해 UTC epoch ms로 변환 (확정: Sysmon UtcTime과 1초 차) | 2016-08-10T16:21:59.550601-0600 → 1470867719550 |
| src_ip | src_endpoint.ip | 그대로. 단 fileinfo는 1-4의 방향 규칙 적용 | 40.80.148.42 |
| src_port | src_endpoint.port | 정수 | 59050 |
| dest_ip | dst_endpoint.ip | 그대로. 단 fileinfo는 1-4 적용 | 192.168.250.70 |
| dest_port | dst_endpoint.port | 정수 | 80 |
| proto | connection_info.protocol_name | 소문자 | TCP → tcp |
| flow_id | connection_info.uid | 문자열. 같은 연결의 http·fileinfo·flow를 잇는 키 | 3326219642 |
| in_iface | unmapped.in_iface | 그대로 | eth1 |
| event_type | (클래스 선택) | flow → 4001, http·fileinfo → 4002, dns → 4003, tls·alert → 이번 범위 밖 | http |
| (상수) | metadata.product.name | 고정값 | Suricata |

### 1-2. flow → Network Activity (4001)

| 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- |
| (상수) | activity_id | 6 (Traffic). flow 이벤트는 연결이 끝난 뒤 한 번 나오는 요약이라서 | 6 |
| flow.start | start_time | 오프셋 반영 UTC epoch ms | 2016-08-28T23:58:58.303376-0600 |
| flow.end | end_time | 오프셋 반영 UTC epoch ms. start보다 이른 값이 실제로 있음(예시 참고) → 그대로 두고 unmapped.flow_time_inverted=true 표시 | 2016-08-28T23:58:58.116152-0600 |
| flow.age | duration | 초 × 1000 | 120 → 120000 |
| flow.bytes_toserver | traffic.bytes_out | 출발지(src) 기준으로 보낸 양 | 49650 |
| flow.bytes_toclient | traffic.bytes_in | 출발지 기준으로 받은 양 | 1163020 |
| flow.pkts_toserver | traffic.packets_out | 정수 | 8 |
| flow.pkts_toclient | traffic.packets_in | 정수 | 4 |
| app_proto | unmapped.app_proto | 그대로 (49%만 있음) | http |
| flow.state, flow.reason | unmapped.flow.state, unmapped.flow.reason | 그대로 | closed, timeout |
| tcp.* | unmapped.tcp.* | 그대로 | tcp_flags=d3 |

### 1-3. http → HTTP Activity (4002)

| 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- |
| http.http_method | http_request.http_method, activity_id | 메서드를 그대로 넣고 activity_id는 GET=3, POST=6, PUT=7, DELETE=2, HEAD=4, OPTIONS=5, CONNECT=1, TRACE=8, 그 외=99 | POST → 6 |
| http.hostname | http_request.url.hostname | 소문자 | imreallynotbatman.com |
| http.url | http_request.url.path, http_request.url.query_string | `?` 앞은 path, 뒤는 query_string(없으면 null). 원문 전체는 url.url_string | /joomla/administrator/index.php |
| http.http_user_agent | http_request.user_agent | 그대로 | MSDW |
| http.http_refer | http_request.referrer | 그대로 (1%만 있음) | http://localhost/joomla/ |
| http.protocol | http_request.version | `HTTP/` 뒤 숫자만 | HTTP/1.1 → 1.1 |
| http.status | http_response.code | 정수 | 200 |
| http.length | http_response.length | 정수 | 0 |
| http.http_content_type | http_response.content_type | 그대로 (30%) | text/plain |
| tx_id | unmapped.tx_id | 같은 연결 안의 요청 순번. fileinfo와 잇는 키 | 0 |

### 1-4. fileinfo → HTTP Activity (4002)

http와 같은 필드(1-3)를 그대로 매핑하고, 아래를 더해요.

| 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- |
| fileinfo.filename | file.name | 경로에서 마지막 `/` 뒤만 name, 전체는 file.path | 3791.exe |
| fileinfo.size | file.size | 정수 | 2705 |
| fileinfo.state, fileinfo.stored, fileinfo.tx_id | unmapped.fileinfo.* | 그대로 | CLOSED |
| src_ip / dest_ip | src_endpoint / dst_endpoint | **방향 주의.** fileinfo의 src→dest는 요청 방향이 아니라 *파일이 흘러간 방향*이에요. 그래서 dest_port가 80·443·8080이 아니고 src_port가 그 포트면 둘을 바꿔서 src=클라이언트, dst=서버로 맞춤. 원래 방향은 unmapped.file_direction(to_server / to_client)에 남김 | 서버 응답: src 192.168.250.70:80 → dest 23.22.63.114:46086 ⇒ 바꿔서 src=23.22.63.114 |

> 확인 필요: OCSF 1.1.0의 HTTP Activity에 `file` 속성이 있는지 schema.ocsf.io에서 확인. 없으면 file.* 대신 unmapped.fileinfo.*에 넣음.

### 1-5. dns → DNS Activity (4003)

Zeek dns와 같은 클래스라 같이 매핑해 둬요.

| 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- |
| dns.type | activity_id | query=1, answer=2 | answer → 2 |
| dns.rrname | query.hostname | 소문자 | kv401-prod.do.dsp.mp.microsoft.com.edgekey.net |
| dns.rrtype | query.type | 그대로 | CNAME |
| dns.id | query.packet_uid | 정수 | 11774 |
| dns.rcode | rcode | 그대로 | NOERROR |
| dns.rdata | answers[].rdata | answer일 때만 | e7589.g.akamaiedge.net |
| dns.ttl | answers[].ttl | 정수 | 20773 |
| dns.tx_id | unmapped.dns.tx_id | 그대로 | 0 |

### 1-6. 이번 범위 밖

| event_type | 처리 | 이유 |
| --- | --- | --- |
| tls | 파서는 건너뜀 (필요해지면 Network Activity + tls 객체) | 이번 라벨 단계에 쓰이지 않음 |
| alert | 파서는 건너뜀 | IDS 자체 탐지라 우리 룰 성능과 섞임. 4주차 신호 형식 회의에서 결정 |

## 2. IIS (`_raw` = W3C 로그 한 줄) → HTTP Activity (4002)

파일에 `#Fields` 머리줄이 없어서 IIS 기본 순서(15개)로 나눠요. 공백으로 나누고, `-`는 null로 바꿔요.

| 순서 | 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- | --- |
| 1+2 | date, time | time | 두 값을 합쳐 **UTC**로 읽음 (확정: 원문 16:37:13 = Splunk _time 10:37:13 MDT) | 2016-08-24 16:37:13 → 1472056633000 |
| 3 | s-ip | dst_endpoint.ip | 그대로 | 192.168.250.70 |
| 4 | cs-method | http_request.http_method, activity_id | 1-3과 같은 표 | GET → 3 |
| 5 | cs-uri-stem | http_request.url.path | 그대로 | / |
| 6 | cs-uri-query | http_request.url.query_string | `-`면 null | - → null |
| 7 | s-port | dst_endpoint.port | 정수 | 80 |
| 8 | cs-username | actor.user.name | `-`면 null. `DOMAIN\user`면 name과 domain으로 나눔 | - → null |
| 9 | c-ip | src_endpoint.ip | 그대로 | 192.168.2.50 |
| 10 | cs(User-Agent) | http_request.user_agent | `+`를 공백으로 바꿈 | Mozilla/4.0 (compatible; MSIE 8.0; ...) |
| 11 | cs(Referer) | http_request.referrer | `-`면 null | - → null |
| 12 | sc-status | http_response.code | 정수 | 416 |
| 13 | sc-substatus | unmapped.sc_substatus | 정수 | 0 |
| 14 | sc-win32-status | unmapped.sc_win32_status | 정수 | 0 |
| 15 | time-taken | duration | 이미 ms | 15 |
| — | result.host | dst_endpoint.hostname, device.hostname | 0절의 예외 규칙 | (검증 때 확인) |

토큰이 15개가 아닌 줄은 파싱하지 않고 unmapped.raw_line에 원문을 넣어 그대로 내보내요. 실제로 2줄(토큰 6개, 10개)이 있어요. 요청 안에 줄바꿈이 섞여 한 기록이 둘로 쪼개진 것으로 보여요(한 줄은 `windows%c0`로 시작하는 경로 조작 페이로드). 이어 붙이지 않고 각각 별도 이벤트로 내보내요.

파일의 마지막 줄 `{"preview":false,"lastrow":true}`는 Splunk export의 끝 표시라 건너뛰어요(raw_ref 줄 번호는 그대로 셈). Suricata·Sysmon 등 다른 BOTS 파일도 같아요.

Splunk가 뽑은 필드 이름(c_ip, cs_method, cs_uri_stem, s_ip, s_port, cs_User_Agent, sc_status, sc_substatus, sc_win32_status, time_taken)이 위 순서와 일치해요. cs-uri-query, cs-username, cs(Referer)는 표본에서 모두 `-`라 Splunk가 뽑지 않았어요.

## 3. AIT russellmitchell (Linux auth · auditd · Apache)

데이터 위치: `ait_lds/russellmitchell/gather/<호스트>/logs/`. 호스트는 intranet_server, vpn, internal_share, inet-firewall. 아래 예시는 intranet_server 기준이에요.

### 3-0. AIT 공통

| 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- |
| (파일 경로 + 줄 번호) | raw_ref | 데이터 폴더 기준 상대 경로, 1부터, `\n`으로만 나눔. **AIT 정답(labels 폴더)의 `line`도 1부터**예요(error.log.2의 1번 줄이 공격자 dirb 요청이고 정답에도 line 1로 있음) | ait_lds/russellmitchell/gather/intranet_server/logs/auth.log:146 |
| (데이터셋 기간) | — | 연도가 없는 로그는 dataset.yaml의 기간(2022-01-21 ~ 2022-01-25)으로 연도를 붙임. 1월 안이라 연도 넘김 문제 없음 | 2022 |
| (상수) | dataset_id | 고정값 | ait_lds_v2 |
| (상수) | scenario_id | 고정값 | russellmitchell |
| labels/<같은 경로>의 `line`, `labels` | label (별도 결합 단계) | 파서는 null. 결합 단계에서 raw_ref 줄 번호와 `line`이 같으면 AIT 정답 이름(예: escalate)을 우리 타임라인 단계로 바꿔 붙임 | {"line": 146, "labels": ["escalate", ...]} |

### 3-1. Apache 접근 로그 → HTTP Activity (4002)

파일: `apache2/<vhost>-access.log*` (combined 형식). 비어 있는 access.log, other_vhosts_access.log는 건너뜀.

| 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- |
| 1번째 (클라이언트 IP) | src_endpoint.ip | 그대로 | 10.143.2.91 |
| 2·3번째 (ident, user) | actor.user.name | user가 `-`면 null | - → null |
| [시각] | time | `+0000` 오프셋 반영해 UTC epoch ms | 24/Jan/2022:07:34:57 +0000 |
| "요청줄"의 메서드 | http_request.http_method, activity_id | Suricata 1-3과 같은 표 | POST → 6 |
| "요청줄"의 URL | http_request.url.path, url.query_string | `?` 앞뒤로 나눔 | /wp-cron.php, doing_wp_cron=1643009698.61 |
| "요청줄"의 프로토콜 | http_request.version | 숫자만 | HTTP/1.1 → 1.1 |
| 상태 코드 | http_response.code | 정수 | 200 |
| 바이트 | http_response.length | 정수, `-`면 null | 6203 |
| "Referer" | http_request.referrer | `-`면 null | http://intranet.smith.russellmitchell.com/ |
| "User-Agent" | http_request.user_agent | 그대로 | Mozilla/5.0 (X11; Ubuntu; ...) |
| (파일 이름의 vhost) | http_request.url.hostname, dst_endpoint.hostname | 파일명 `-access.log` 앞부분 | intranet.smith.russellmitchell.com |
| (폴더의 호스트) | device.hostname | 폴더 이름의 `_`를 `-`로 (syslog 표기와 맞춤) | intranet_server → intranet-server |

형식에 맞지 않는 줄은 unmapped.raw_line으로 내보내요.

### 3-2. Apache 오류 로그 → HTTP Activity (4002), 선택

파일: `apache2/<vhost>-error.log*`. AIT 정답이 dirb 디렉터리 탐색(T1595.003)을 이 파일에 붙여 둬서 넣어요.

| 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- |
| [요일 월 일 시각 연도] | time | 오프셋이 없음 → access 로그와 같은 UTC로 읽음 | Mon Jan 24 03:57:26.696483 2022 |
| [모듈:수준] | severity, unmapped.module | error → 4, warn → 3, notice → 1 | authz_core:error |
| [client IP:포트] | src_endpoint.ip, src_endpoint.port | 없으면 null | 172.19.131.174:36072 |
| 나머지 메시지 | message | 그대로 | AH01630: client denied by server configuration: /var/www/.../.hta |
| (상수) | activity_id | 99 (Other). 메서드가 없음 | 99 |

### 3-3. auth.log (syslog)

머리 부분 `월 일 시각 호스트 프로그램[pid]: 내용`을 먼저 나누고, 프로그램별로 클래스를 정해요.

| 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- |
| 월 일 시각 | time | 3-0의 연도를 붙여 **UTC**로 읽음 (auth.log 마지막 23:39:01과 audit.log 마지막 epoch 23:39:13이 맞음) | Jan 24 04:37:58 → 2022-01-24T04:37:58Z |
| 호스트 | device.hostname | 소문자 | intranet-server |
| 프로그램[pid] | metadata.log_name, process.pid (프로그램 실행 기록일 때) | 대괄호 안 숫자 | su[27950] |

프로그램별 처리:

| 프로그램 | 클래스 | 매핑 | 예시 |
| --- | --- | --- | --- |
| **sudo** | Process Activity (1007), activity_id=1 Launch | `사용자 :` 앞 → actor.user.name, `USER=` → process.user.name, `COMMAND=` → process.cmd_line, `TTY=` → unmapped.tty, `PWD=` → process.file.parent_folder | `jhall : TTY=pts/1 ; PWD=/var/www/.../uploads/2022/01 ; USER=root ; COMMAND=list` → actor=jhall, user=root, cmd_line=list |
| **su** | Authentication (3002), activity_id=1 Logon | `Successful su for A by B` → user.name=A, actor.user.name=B, status=Success. `FAILED su` → status=Failure. auth_protocol=su | `Successful su for jhall by www-data` |
| **sshd** | Authentication (3002) | `Accepted <방식> for <user> from <IP> port <n>` → status=Success, user.name, src_endpoint.ip, auth_protocol=<방식>(password, publickey). `Failed password ...` → status=Failure. `session opened/closed` → activity_id 1/2 | `session closed for user jhall` → Logoff, user=jhall |
| systemd-logind, systemd | 건너뜀 | 세션 관리 잡음 | Removed session 111. |
| CRON | 건너뜀 | 전체의 95%를 차지하는 정기 작업 | session closed for user root |

> 팀원 1 확인용: T1548.003 룰에 필요한 필드는 **actor.user.name(sudo를 실행한 사람), process.user.name(대상 계정), process.cmd_line(명령)** 세 개이고 모두 채워져요. intranet_server의 auditd에는 명령 실행 기록(EXECVE, USER_CMD)이 표본에 없어서, sudo 근거는 auth.log가 주 소스예요.

### 3-4. audit.log (auditd)

한 줄이 레코드 하나예요. 같은 사건의 여러 줄(SYSCALL, PROCTITLE 등)은 `msg=audit(시각:번호)`의 번호가 같지만, AIT 정답이 줄마다 따로 붙어 있어서 **묶지 않고 한 줄 = 이벤트 하나**로 내보내요. 묶음 번호는 unmapped.audit_serial에 남겨요.

| 원본 필드 | OCSF 필드 | 변환 규칙 | 예시 값 |
| --- | --- | --- | --- |
| type | (클래스 선택) | USER_LOGIN·USER_AUTH → Authentication, USER_CMD·EXECVE·SYSCALL → Process Activity, 나머지(CRED_*, USER_START/END/ACCT, LOGIN, SERVICE_*, AVC) → 건너뜀 | USER_LOGIN |
| msg=audit(시각:번호) | time, unmapped.audit_serial | 시각은 epoch 초 → × 1000 (이미 UTC) | 1642761574.840 → 1642761574840 |
| pid, ppid | process.pid, process.parent_process.pid | 정수 | 14362 |
| uid, auid | actor.user.uid, unmapped.auid | auid 4294967295는 "로그인 안 함" → null | 1002 |
| acct, id | user.name / user.uid | 따옴표 제거 | jhall |
| exe | process.file.path | 따옴표 제거 | /usr/sbin/sshd |
| hostname, addr | src_endpoint.ip (IP일 때), src_endpoint.hostname (이름일 때) | `?`는 null | 172.19.131.174 |
| terminal | unmapped.terminal | `?`는 null | /dev/pts/0 |
| res | status | success → Success, failed → Failure, 1 → Success | success |
| proctitle | process.cmd_line | 16진수면 풀어서 NUL을 공백으로 | 61707061... → apparmor_parser -r -T -W ... |
| ses, op, 나머지 | unmapped.* | 그대로 | op=login |

### 3-5. AIT에서 범위 밖

| 파일 | 이유 |
| --- | --- |
| suricata/fast.log | EVE가 아니라 경보만 남는 한 줄 텍스트. BOTS의 alert와 같은 이유로 제외 |
| syslog.* | 일반 시스템 메시지. 필요해지면 추가 |
| dnsmasq.log, openvpn.log | AIT 정답이 붙어 있음(dnsteal, attacker_vpn). DNS Activity·Authentication 후보라 4주차에 별도 검토 |

## 4. 검증 기록

| 항목 | 결과 |
| --- | --- |
| Suricata 시간 | 확정. Sysmon UtcTime 22:21:58 = Suricata flow.end 16:21:59-0600 (1초 차) |
| IIS 시간대 | 확정. UTC (원문 16:37:13 = _time 10:37:13 MDT) |
| IIS 필드 순서 | 확정. 22,615줄 중 22,613줄이 15개 토큰, Splunk 추출 필드 이름과 순서 일치. 깨진 2줄은 raw_line으로 |
| IIS 날짜 범위 | 2016-08-10 22,399줄(웹사이트 변조), 2016-08-24 214줄(Cerber). 변조 시나리오는 Suricata와 IIS 두 곳에 HTTP 근거가 있음 |
| HTTP Activity의 file 속성 | 미확인 |
| AIT 정답 줄 번호 | 확정. 1부터 (error.log.2 line 1 = 공격자 dirb 요청) |
| AIT auth.log 시간대 | 사실상 확정. UTC (auth.log 끝 Jan 24 23:39:01, audit.log 끝 epoch = 23:39:13Z) |
| AIT 공격자 IP 단서 | 172.19.131.174 (dirb 요청, sshd 로그인 USER_LOGIN의 addr) |
