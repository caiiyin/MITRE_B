# 필드 목록: combined_zeek.log (형식 JSON, 2141줄)

## conn (613건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | conn |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588205199.82437 |
| uid | 100% | Cvf4XX17hSAgXDdGEd |
| id_orig_h | 100% | 10.0.1.6 |
| id_orig_p | 100% | 54243 |
| id_resp_h | 100% | 10.0.0.4 |
| id_resp_p | 100% | 53 |
| proto | 100% | udp |
| conn_state | 100% | SF |
| missed_bytes | 100% | 0 |
| history | 100% | Dd |
| orig_pkts | 100% | 1 |
| orig_ip_bytes | 100% | 67 |
| resp_pkts | 100% | 1 |
| resp_ip_bytes | 100% | 83 |
| orig_l2_addr | 100% | 00:0d:3a:13:e3:69 |
| resp_l2_addr | 100% | 12:34:56:78:9a:bc |
| duration | 94% | 0.001528024673461914 |
| orig_bytes | 94% | 39 |
| resp_bytes | 94% | 55 |
| service | 80% | dns |

## files (448건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | files |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588206049.300416 |
| fuid | 100% | FZ7E9x2gD5KHc8KoDg |
| tx_hosts | 100% | ["10.0.0.4"] |
| rx_hosts | 100% | ["10.0.1.6"] |
| conn_uids | 100% | ["CF37FuG0Jho600cAa"] |
| source | 100% | SMB |
| depth | 100% | 0 |
| analyzers | 100% | ["MD5", "SHA1"] |
| mime_type | 100% | text/ini |
| duration | 100% | 0.0 |
| is_orig | 100% | False |
| seen_bytes | 100% | 22 |
| missing_bytes | 100% | 0 |
| overflow_bytes | 100% | 0 |
| timedout | 100% | False |
| md5 | 99% | cc85d7649546d3c0b1607f761b73fec2 |
| sha1 | 99% | 1a1a10b819f321b91b47d7dd73668406a15992db |
| total_bytes | 15% | 22 |
| filename | 1% | dmevals.local\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9 |
| extracted | 0% | HTTP-FV8BmBzhLupORXNNc.exe |
| extracted_cutoff | 0% | False |

## ssl (378건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | ssl |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588207244.736422 |
| uid | 100% | CpnezL3085IfcJzSAe |
| id_orig_h | 100% | 10.0.1.6 |
| id_orig_p | 100% | 57091 |
| id_resp_h | 100% | 192.168.0.4 |
| id_resp_p | 100% | 8443 |
| version | 100% | TLSv12 |
| cipher | 100% | TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 |
| curve | 100% | secp256r1 |
| resumed | 100% | False |
| established | 100% | True |
| cert_chain_fuids | 100% | ["F1v6sJmRC73GU6WT3"] |
| client_cert_chain_fuids | 100% | [] |
| subject | 100% | emailAddress=synthesize@rempel.group.net,CN=rempel.group.net |
| issuer | 100% | emailAddress=synthesize@rempel.group.net,CN=rempel.group.net |
| validation_status | 100% | self signed certificate |
| resp_certificate_sha1 | 100% | d9105746ea023ecdc6a47e7b4d026d5308525b8c |
| ja3 | 100% | e0fe397a5edfba9a6facc7c7b341f4eb |
| ja3s | 100% | e35df3e00ca4ef31d42b34bebaa2f86e |
| server_name | 99% | 192.168.0.4 |

## x509 (378건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | x509 |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588207244.736422 |
| id | 100% | F1v6sJmRC73GU6WT3 |
| certificate_version | 100% | 3 |
| certificate_serial | 100% | 7EFDE1CFECCCDB44 |
| certificate_subject | 100% | emailAddress=synthesize@rempel.group.net,CN=rempel.group.net |
| certificate_issuer | 100% | emailAddress=synthesize@rempel.group.net,CN=rempel.group.net |
| certificate_not_valid_before | 100% | 1470462331.0 |
| certificate_not_valid_after | 100% | 1722750331.0 |
| certificate_key_alg | 100% | rsaEncryption |
| certificate_sig_alg | 100% | sha256WithRSAEncryption |
| certificate_key_type | 100% | rsa |
| certificate_key_length | 100% | 2048 |
| certificate_exponent | 100% | 65537 |
| basic_constraints_ca | 100% | True |

## dce_rpc (123건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | dce_rpc |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588206048.592985 |
| uid | 100% | CAGQDqsQlWvA6qoV5 |
| id_orig_h | 100% | 10.0.1.6 |
| id_orig_p | 100% | 56953 |
| id_resp_h | 100% | 10.0.0.4 |
| id_resp_p | 100% | 135 |
| rtt | 100% | 0.0008161067962646484 |
| named_pipe | 100% | 135 |
| endpoint | 100% | epmapper |
| operation | 100% | ept_map |

## http (62건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | http |
| @system | 100% | simplerockbuild.simplerock.lan |
| @proc | 100% | zeek |
| ts | 100% | 1588206738.09551 |
| uid | 100% | ChOJWf3yQbPwENbBK1 |
| id_orig_h | 100% | 10.0.1.4 |
| id_orig_p | 100% | 60757 |
| id_resp_h | 100% | 192.168.0.4 |
| id_resp_p | 100% | 80 |
| trans_depth | 100% | 1 |
| method | 100% | OPTIONS |
| host | 100% | 192.168.0.4 |
| uri | 100% | / |
| version | 100% | 1.1 |
| user_agent | 100% | DavClnt |
| request_body_len | 100% | 0 |
| response_body_len | 100% | 209 |
| status_code | 100% | 403 |
| status_msg | 100% | Forbidden |
| tags | 100% | [] |
| client_header_names | 100% | ["CONNECTION", "USER-AGENT", "TRANSLATE", "HOST"] |
| resp_fuids | 83% | ["F7rWMf1rWbywzkeiU"] |
| resp_mime_types | 83% | ["text/html"] |
| orig_fuids | 19% | ["FYhBZX1o5kQrnfPbf5"] |
| orig_mime_types | 19% | ["application/xml"] |

## dns (53건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | dns |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588205199.82437 |
| uid | 100% | Cvf4XX17hSAgXDdGEd |
| id_orig_h | 100% | 10.0.1.6 |
| id_orig_p | 100% | 54243 |
| id_resp_h | 100% | 10.0.0.4 |
| id_resp_p | 100% | 53 |
| proto | 100% | udp |
| trans_id | 100% | 41180 |
| query | 100% | newyork.dmevals.local |
| qclass | 100% | 1 |
| qclass_name | 100% | C_INTERNET |
| qtype | 100% | 1 |
| qtype_name | 100% | A |
| AA | 100% | True |
| TC | 100% | False |
| RD | 100% | True |
| RA | 100% | True |
| Z | 100% | 0 |
| rejected | 100% | False |
| rcode | 69% | 0 |
| rcode_name | 69% | NOERROR |
| rtt | 47% | 0.001528024673461914 |
| answers | 47% | ["10.0.0.4"] |
| TTLs | 47% | [3600.0] |

## kerberos (35건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | kerberos |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588205199.832602 |
| uid | 100% | CJ21Le4zsTUcyKKi98 |
| id_orig_h | 100% | 10.0.1.6 |
| id_orig_p | 100% | 56880 |
| id_resp_h | 100% | 10.0.0.4 |
| id_resp_p | 100% | 445 |
| request_type | 71% | AS |
| client | 71% | pbeesly/dmevals |
| service | 71% | krbtgt/dmevals |
| success | 71% | False |
| till | 71% | 2136422885.0 |
| forwardable | 71% | True |
| renewable | 71% | True |
| cipher | 51% | aes256-cts-hmac-sha1-96 |
| error_msg | 20% | KDC_ERR_PREAUTH_REQUIRED |

## dpd (12건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | dpd |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588206925.629572 |
| uid | 100% | CE5Tb74JHZJJsCpgH8 |
| id_orig_h | 100% | 10.0.1.4 |
| id_orig_p | 100% | 60803 |
| id_resp_h | 100% | 10.0.1.6 |
| id_resp_p | 100% | 445 |
| proto | 100% | tcp |
| analyzer | 100% | SMB |
| failure_reason | 100% | Binpac exception: binpac exception: invalid index for case:  |

## smb_files (12건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | smb_files |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588206049.298765 |
| uid | 100% | CF37FuG0Jho600cAa |
| id_orig_h | 100% | 10.0.1.6 |
| id_orig_p | 100% | 56957 |
| id_resp_h | 100% | 10.0.0.4 |
| id_resp_p | 100% | 445 |
| action | 100% | SMB::FILE_OPEN |
| path | 100% | \\NEWYORK.dmevals.local\sysvol |
| name | 100% | dmevals.local\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9 |
| size | 100% | 22 |
| times_modified | 100% | 1588187906.664602 |
| times_accessed | 100% | 1588187906.664602 |
| times_created | 100% | 1588187906.664602 |
| times_changed | 100% | 1588187912.7667403 |

## weird (12건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | weird |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588205199.832602 |
| name | 100% | ip_hdr_len_zero |
| notice | 100% | False |
| peer | 100% | zeek |
| uid | 25% | ChKSSW69C5g1bfSuc |
| id_orig_h | 25% | 10.0.1.6 |
| id_orig_p | 25% | 57025 |
| id_resp_h | 25% | 10.0.0.4 |
| id_resp_p | 25% | 49667 |
| addl | 25% | 68 |

## smb_mapping (11건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | smb_mapping |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588205199.835004 |
| uid | 100% | CJ21Le4zsTUcyKKi98 |
| id_orig_h | 100% | 10.0.1.6 |
| id_orig_p | 100% | 56880 |
| id_resp_h | 100% | 10.0.0.4 |
| id_resp_p | 100% | 445 |
| path | 100% | \\NEWYORK.dmevals.local\IPC$ |
| share_type | 100% | PIPE |

## notice (2건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | notice |
| @system | 100% | bobs.bigwheel.local |
| @proc | 100% | zeek |
| ts | 100% | 1588207244.740518 |
| uid | 100% | CpnezL3085IfcJzSAe |
| id_orig_h | 100% | 10.0.1.6 |
| id_orig_p | 100% | 57091 |
| id_resp_h | 100% | 192.168.0.4 |
| id_resp_p | 100% | 8443 |
| fuid | 100% | F1v6sJmRC73GU6WT3 |
| proto | 100% | tcp |
| note | 100% | SSL::Invalid_Server_Cert |
| msg | 100% | SSL certificate validation failed with (self signed certific |
| sub | 100% | emailAddress=synthesize@rempel.group.net,CN=rempel.group.net |
| src | 100% | 10.0.1.6 |
| dst | 100% | 192.168.0.4 |
| p | 100% | 8443 |
| actions | 100% | ["Notice::ACTION_LOG"] |
| suppress_for | 100% | 3600.0 |

## pe (1건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| @stream | 100% | pe |
| @system | 100% | simplerockbuild.simplerock.lan |
| @proc | 100% | zeek |
| ts | 100% | 1588206925.659819 |
| id | 100% | FV8BmBzhLupORXNNc |
| machine | 100% | AMD64 |
| compile_ts | 100% | 1536071929.0 |
| os | 100% | Windows XP x64 or Server 2003 |
| subsystem | 100% | WINDOWS_CUI |
| is_exe | 100% | True |
| is_64bit | 100% | True |
| uses_aslr | 100% | True |
| uses_dep | 100% | True |
| uses_code_integrity | 100% | False |
| uses_seh | 100% | True |
| has_import_table | 100% | True |
| has_export_table | 100% | False |
| has_cert_table | 100% | False |
| has_debug_data | 100% | False |
| section_names | 100% | ["UPX0", "UPX1", ".rsrc"] |

## 첫 3줄 원문

```
{"@stream":"conn","@system":"bobs.bigwheel.local","@proc":"zeek","ts":1588205199.82437,"uid":"Cvf4XX17hSAgXDdGEd","id_orig_h":"10.0.1.6","id_orig_p":54243,"id_resp_h":"10.0.0.4","id_resp_p":53,"proto":"udp","service":"dns","duration":0.001528024673461914,"orig_bytes":39,"resp_bytes":55,"conn_state":"SF","missed_bytes":0,"history":"Dd","orig_pkts":1,"orig_ip_bytes":67,"resp_pkts":1,"resp_ip_bytes":
{"@stream":"conn","@system":"bobs.bigwheel.local","@proc":"zeek","ts":1588205199.827696,"uid":"CJ21Le4zsTUcyKKi98","id_orig_h":"10.0.1.6","id_orig_p":56880,"id_resp_h":"10.0.0.4","id_resp_p":445,"proto":"tcp","service":"gssapi,smb,krb","duration":10.761076927185059,"orig_bytes":4020,"resp_bytes":1681,"conn_state":"RSTO","missed_bytes":0,"history":"ShADdaR","orig_pkts":12,"orig_ip_bytes":1307,"resp
{"@stream":"conn","@system":"bobs.bigwheel.local","@proc":"zeek","ts":1588205279.953876,"uid":"CnOP7t1eGGHf6LFfuk","id_orig_h":"10.0.1.6","id_orig_p":65108,"id_resp_h":"10.0.0.4","id_resp_p":53,"proto":"udp","service":"dns","duration":0.0015990734100341797,"orig_bytes":36,"resp_bytes":104,"conn_state":"SF","missed_bytes":0,"history":"Dd","orig_pkts":1,"orig_ip_bytes":64,"resp_pkts":1,"resp_ip_byte
```
