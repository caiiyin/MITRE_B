# 필드 목록: botsv1.suricata.json.gz

앞 500000줄 기준, 종류별 최대 500건 표본

## flow (251664건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| app_proto | 49% | dns |
| dest_ip | 100% | 192.168.229.240 |
| dest_port | 100% | 9997 |
| event_type | 100% | flow |
| flow.age | 100% | 1 |
| flow.bytes_toclient | 100% | 252 |
| flow.bytes_toserver | 100% | 492 |
| flow.end | 100% | 2016-08-28T23:58:58.116152-0600 |
| flow.pkts_toclient | 100% | 4 |
| flow.pkts_toserver | 100% | 8 |
| flow.reason | 100% | timeout |
| flow.start | 100% | 2016-08-28T23:58:58.303376-0600 |
| flow.state | 100% | closed |
| flow_id | 100% | 786872163 |
| proto | 100% | TCP |
| src_ip | 100% | 192.168.230.74 |
| src_port | 100% | 59050 |
| tcp.ack | 64% | True |
| tcp.cwr | 39% | True |
| tcp.ecn | 39% | True |
| tcp.fin | 64% | True |
| tcp.psh | 25% | True |
| tcp.rst | 22% | True |
| tcp.state | 64% | closed |
| tcp.syn | 64% | True |
| tcp.tcp_flags | 66% | d3 |
| tcp.tcp_flags_tc | 66% | 53 |
| tcp.tcp_flags_ts | 66% | d3 |
| timestamp | 100% | 2016-08-28T23:58:58.000072-0600 |

## dns (182760건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| dest_ip | 100% | 192.168.225.125 |
| dest_port | 100% | 53338 |
| dns.id | 100% | 11774 |
| dns.rcode | 66% | NOERROR |
| dns.rdata | 29% | e7589.g.akamaiedge.net |
| dns.rrname | 99% | kv401-prod.do.dsp.mp.microsoft.com.edgekey.net |
| dns.rrtype | 78% | CNAME |
| dns.ttl | 45% | 20773 |
| dns.tx_id | 33% | 0 |
| dns.type | 100% | answer |
| event_type | 100% | dns |
| flow_id | 100% | 3560840892 |
| in_iface | 100% | eth1 |
| proto | 100% | UDP |
| src_ip | 100% | 8.8.8.8 |
| src_port | 100% | 53 |
| timestamp | 100% | 2016-08-28T23:58:59.931869-0600 |

## tls (62613건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| dest_ip | 100% | 192.168.225.203 |
| dest_port | 100% | 8089 |
| event_type | 100% | tls |
| flow_id | 100% | 3525056877 |
| in_iface | 100% | eth1 |
| proto | 100% | TCP |
| src_ip | 100% | 192.168.230.20 |
| src_port | 100% | 50905 |
| timestamp | 100% | 2016-08-28T23:58:51.464001-0600 |
| tls.fingerprint | 100% | 02:67:29:0d:e5:ec:8b:e0:fb:b4:bf:55:c6:62:21:00:1a:17:4e:b6 |
| tls.issuerdn | 100% | C=US, ST=CA, L=San Francisco, O=Splunk, CN=SplunkCommonCA/em |
| tls.sni | 15% | kv401-prod.do.dsp.mp.microsoft.com |
| tls.subject | 100% | CN=SplunkServerDefaultCert/O=SplunkUser |
| tls.version | 100% | TLS 1.2 |

## http (1529건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| dest_ip | 100% | 207.46.101.29 |
| dest_port | 100% | 80 |
| event_type | 100% | http |
| flow_id | 100% | 1459680372 |
| http.hostname | 97% | ssw.live.com |
| http.http_content_type | 30% | text/plain |
| http.http_method | 98% | POST |
| http.http_refer | 1% | http://localhost/joomla/ |
| http.http_user_agent | 94% | MSDW |
| http.length | 100% | 0 |
| http.protocol | 98% | HTTP/1.1 |
| http.status | 99% | 200 |
| http.url | 98% | /UploadData.aspx |
| in_iface | 96% | eth1 |
| proto | 100% | TCP |
| src_ip | 100% | 192.168.225.215 |
| src_port | 100% | 2800 |
| timestamp | 100% | 2016-08-28T23:58:56.845196-0600 |
| tx_id | 100% | 0 |

## fileinfo (1434건)

| 원본 필드 | 나온 비율 | 예시 값 |
| --- | --- | --- |
| app_proto | 100% | http |
| dest_ip | 100% | 134.170.104.154 |
| dest_port | 100% | 80 |
| event_type | 100% | fileinfo |
| fileinfo.filename | 100% | /UploadData.aspx |
| fileinfo.size | 100% | 1460 |
| fileinfo.state | 100% | CLOSED |
| fileinfo.stored | 100% | False |
| fileinfo.tx_id | 100% | 0 |
| flow_id | 100% | 1871036844 |
| http.hostname | 98% | ssw.live.com |
| http.http_content_type | 18% | text/xml |
| http.http_method | 98% | POST |
| http.http_refer | 0% | http://localhost/joomla/ |
| http.http_user_agent | 96% | MSDW |
| http.length | 100% | 0 |
| http.protocol | 98% | HTTP/1.1 |
| http.status | 100% | 200 |
| http.url | 98% | /UploadData.aspx |
| in_iface | 97% | eth1 |
| proto | 100% | TCP |
| src_ip | 100% | 192.168.225.170 |
| src_port | 100% | 19631 |
| timestamp | 100% | 2016-08-28T23:56:34.238309-0600 |

