# AIT russellmitchell 필드 목록 (intranet_server)

## dataset.yaml
```
name: processed_russellmitchell_scenario
start: '2022-01-21T00:00:00'
end: '2022-01-25T00:00:00'

```

## 파일 목록

- gather\intranet_server\logs\apache2\access.log (0 KB)
- gather\intranet_server\logs\apache2\error.log.1 (0 KB)
- gather\intranet_server\logs\apache2\error.log.2 (277 KB)
- gather\intranet_server\logs\apache2\error.log.3 (0 KB)
- gather\intranet_server\logs\apache2\error.log.4 (0 KB)
- gather\intranet_server\logs\apache2\intranet.smith.russellmitchell.com-access.log (0 KB)
- gather\intranet_server\logs\apache2\intranet.smith.russellmitchell.com-access.log.1 (145 KB)
- gather\intranet_server\logs\apache2\intranet.smith.russellmitchell.com-access.log.2 (1528 KB)
- gather\intranet_server\logs\apache2\intranet.smith.russellmitchell.com-access.log.3 (250 KB)
- gather\intranet_server\logs\apache2\intranet.smith.russellmitchell.com-access.log.4 (282 KB)
- gather\intranet_server\logs\apache2\intranet.smith.russellmitchell.com-error.log (0 KB)
- gather\intranet_server\logs\apache2\intranet.smith.russellmitchell.com-error.log.1 (0 KB)
- gather\intranet_server\logs\apache2\intranet.smith.russellmitchell.com-error.log.2 (8 KB)
- gather\intranet_server\logs\apache2\intranet.smith.russellmitchell.com-error.log.3 (0 KB)
- gather\intranet_server\logs\apache2\other_vhosts_access.log (0 KB)
- gather\intranet_server\logs\audit\audit.log (410 KB)
- gather\intranet_server\logs\auth.log (27 KB)
- gather\intranet_server\logs\auth.log.1 (35 KB)
- gather\intranet_server\logs\suricata\fast.log (9 KB)
- gather\intranet_server\logs\syslog.1 (14 KB)
- gather\intranet_server\logs\syslog.2 (23 KB)
- gather\intranet_server\logs\syslog.3 (20 KB)
- gather\intranet_server\logs\syslog.4 (46 KB)

## auth.log (272줄, Jan 23 06:25:05 ~ Jan 24 23:39:01)

| 프로그램 | 줄 수 | 예시 |
| --- | --- | --- |
| CRON | 257 | `Jan 23 06:25:05 intranet-server CRON[22883]: pam_unix(cron:session): session closed for user root` |
| sshd | 4 | `Jan 23 16:23:04 intranet-server sshd[15014]: pam_unix(sshd:session): session closed for user jhall` |
| sudo | 4 | `Jan 24 04:37:58 intranet-server sudo:    jhall : TTY=pts/1 ; PWD=/var/www/intranet.smith.russellmitchell.com/wp-content/uploads/2022/01 ; USER=root ; COMMAND=list` |
| systemd-logind | 3 | `Jan 23 16:23:04 intranet-server systemd-logind[957]: Removed session 111.` |
| su | 3 | `Jan 24 04:37:40 intranet-server su[27950]: Successful su for jhall by www-data` |
| systemd | 1 | `Jan 23 16:30:47 intranet-server systemd: pam_unix(systemd-user:session): session opened for user jhall by (uid=0)` |

## audit.log (앞 300000줄, epoch 1642723741.072 ~ 1643067553.266)

### CRED_ACQ (308줄)

키: pid, uid, auid, ses, msg, op, acct, exe, hostname, addr, terminal, res

`type=CRED_ACQ msg=audit(1642723741.072:376): pid=10125 uid=0 auid=4294967295 ses=4294967295 msg='op=PAM:setcred acct="root" exe="/usr/sbin/cron" hostname=? addr=? terminal=cron res=success'`

### USER_START (306줄)

키: pid, uid, auid, ses, msg, op, acct, exe, hostname, addr, terminal, res

`type=USER_START msg=audit(1642723741.080:378): pid=10125 uid=0 auid=0 ses=65 msg='op=PAM:session_open acct="root" exe="/usr/sbin/cron" hostname=? addr=? terminal=cron res=success'`

### USER_ACCT (305줄)

키: pid, uid, auid, ses, msg, op, acct, exe, hostname, addr, terminal, res

`type=USER_ACCT msg=audit(1642723741.072:375): pid=10125 uid=0 auid=4294967295 ses=4294967295 msg='op=PAM:accounting acct="root" exe="/usr/sbin/cron" hostname=? addr=? terminal=cron res=success'`

### LOGIN (304줄)

키: auid, ses, pid, uid, tty, res

`type=LOGIN msg=audit(1642723741.076:377): pid=10125 uid=0 old-auid=4294967295 auid=0 tty=(none) old-ses=4294967295 ses=65 res=1`

### CRED_DISP (302줄)

키: pid, uid, auid, ses, msg, op, acct, exe, hostname, addr, terminal, res

`type=CRED_DISP msg=audit(1642723741.084:379): pid=10125 uid=0 auid=0 ses=65 msg='op=PAM:setcred acct="root" exe="/usr/sbin/cron" hostname=? addr=? terminal=cron res=success'`

### USER_END (302줄)

키: pid, uid, auid, ses, msg, op, acct, exe, hostname, addr, terminal, res

`type=USER_END msg=audit(1642723741.084:380): pid=10125 uid=0 auid=0 ses=65 msg='op=PAM:session_close acct="root" exe="/usr/sbin/cron" hostname=? addr=? terminal=cron res=success'`

### SERVICE_START (241줄)

키: pid, uid, auid, ses, msg, unit, comm, exe, hostname, addr, terminal, res

`type=SERVICE_START msg=audit(1642723752.624:381): pid=1 uid=0 auid=4294967295 ses=4294967295 msg='unit=phpsessionclean comm="systemd" exe="/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'`

### SERVICE_STOP (230줄)

키: pid, uid, auid, ses, msg, unit, comm, exe, hostname, addr, terminal, res

`type=SERVICE_STOP msg=audit(1642723752.624:382): pid=1 uid=0 auid=4294967295 ses=4294967295 msg='unit=phpsessionclean comm="systemd" exe="/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'`

### AVC (4줄)

키: apparmor, operation, info, profile, name, pid, comm

`type=AVC msg=audit(1642746582.129:529): apparmor="STATUS" operation="profile_replace" info="same as current profile, skipping" profile="unconfined" name="/sbin/dhclient" pid=23662 comm="apparmor_parser"`

### SYSCALL (4줄)

키: arch, syscall, success, exit, a0, a1, a2, a3, items, ppid, pid, auid, uid, gid, euid, suid, fsuid, egid, sgid, fsgid, tty, ses, comm, exe, key

`type=SYSCALL msg=audit(1642746582.129:529): arch=c000003e syscall=1 success=yes exit=44953 a0=6 a1=55688bbf9b10 a2=af99 a3=0 items=0 ppid=23661 pid=23662 auid=4294967295 uid=0 gid=0 euid=0 suid=0 fsuid=0 egid=0 sgid=0 fs`

### PROCTITLE (4줄)

키: proctitle

`type=PROCTITLE msg=audit(1642746582.129:529): proctitle=61707061726D6F725F706172736572002D72002D54002D57002F6574632F61707061726D6F722E642F7362696E2E6468636C69656E74`

### USER_LOGIN (3줄)

키: pid, uid, auid, ses, msg, op, id, exe, hostname, addr, terminal, res

`type=USER_LOGIN msg=audit(1642761574.840:683): pid=14362 uid=0 auid=1002 ses=100 msg='op=login id=1002 exe="/usr/sbin/sshd" hostname=172.19.131.174 addr=172.19.131.174 terminal=/dev/pts/0 res=success'`


## apache2 (각 파일 앞 3줄)

### access.log
```

```
### error.log.1
```
[Mon Jan 24 06:25:03.954255 2022] [mpm_prefork:notice] [pid 449] AH00163: Apache/2.4.29 (Ubuntu) OpenSSL/1.1.1 configured -- resuming normal operations
[Mon Jan 24 06:25:03.954309 2022] [core:notice] [pid 449] AH00094: Command line: '/usr/sbin/apache2'

```
### error.log.2
```
[Sun Jan 23 06:25:03.376337 2022] [mpm_prefork:notice] [pid 449] AH00163: Apache/2.4.29 (Ubuntu) OpenSSL/1.1.1 configured -- resuming normal operations
[Sun Jan 23 06:25:03.376375 2022] [core:notice] [pid 449] AH00094: Command line: '/usr/sbin/apache2'
TERM environment variable not set.
```
### error.log.3
```
[Sat Jan 22 06:25:04.223068 2022] [mpm_prefork:notice] [pid 449] AH00163: Apache/2.4.29 (Ubuntu) OpenSSL/1.1.1 configured -- resuming normal operations
[Sat Jan 22 06:25:04.223105 2022] [core:notice] [pid 449] AH00094: Command line: '/usr/sbin/apache2'
[Sun Jan 23 06:25:03.170832 2022] [mpm_prefork:notice] [pid 449] AH00171: Graceful restart requested, doing restart
```
### error.log.4
```
[Sat Jan 22 06:25:03.565696 2022] [mpm_prefork:notice] [pid 449] AH00171: Graceful restart requested, doing restart

```
### intranet.smith.russellmitchell.com-access.log
```

```
### intranet.smith.russellmitchell.com-access.log.1
```
10.143.2.91 - - [24/Jan/2022:07:34:57 +0000] "GET / HTTP/1.1" 200 6203 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
10.143.2.4 - - [24/Jan/2022:07:34:58 +0000] "POST /wp-cron.php?doing_wp_cron=1643009698.6149239540100097656250 HTTP/1.1" 200 150 "-" "WordPress/5.8.3; https://intranet.smith.russellmitchell.com"
10.143.2.91 - - [24/Jan/2022:07:34:58 +0000] "GET /wp-includes/css/dist/block-library/style.min.css?ver=5.8.3 HTTP/1.1" 200 10846 "http://intranet.smith.russellmitchell.com/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
```
### intranet.smith.russellmitchell.com-access.log.2
```
10.143.2.91 - - [23/Jan/2022:06:36:13 +0000] "GET / HTTP/1.1" 200 6203 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
10.143.2.91 - - [23/Jan/2022:06:36:14 +0000] "GET /wp-includes/css/dist/block-library/style.min.css?ver=5.8.3 HTTP/1.1" 200 10846 "http://intranet.smith.russellmitchell.com/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
10.143.2.91 - - [23/Jan/2022:06:36:14 +0000] "GET /wp-includes/js/wp-embed.min.js?ver=5.8.3 HTTP/1.1" 200 1099 "http://intranet.smith.russellmitchell.com/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
```
### intranet.smith.russellmitchell.com-access.log.3
```
10.143.2.4 - - [22/Jan/2022:07:26:48 +0000] "POST /wp-cron.php?doing_wp_cron=1642836408.1728169918060302734375 HTTP/1.1" 200 150 "-" "WordPress/5.8.3; https://intranet.smith.russellmitchell.com"
10.143.2.25 - - [22/Jan/2022:07:26:47 +0000] "GET / HTTP/1.1" 200 6202 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/97.0.4692.71 Safari/537.36"
10.143.2.25 - - [22/Jan/2022:07:26:48 +0000] "GET /wp-includes/js/wp-embed.min.js?ver=5.8.3 HTTP/1.1" 200 1099 "http://intranet.smith.russellmitchell.com/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/97.0.4692.71 Safari/537.36"
```
### intranet.smith.russellmitchell.com-access.log.4
```
10.143.3.65 - - [21/Jan/2022:05:55:22 +0000] "GET / HTTP/1.1" 200 6202 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
10.143.3.65 - - [21/Jan/2022:05:55:27 +0000] "GET /wp-includes/css/dist/block-library/style.min.css?ver=5.8.3 HTTP/1.1" 200 10846 "http://intranet.smith.russellmitchell.com/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
10.143.3.65 - - [21/Jan/2022:05:55:27 +0000] "GET /wp-includes/js/wp-embed.min.js?ver=5.8.3 HTTP/1.1" 200 1099 "http://intranet.smith.russellmitchell.com/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
```
### intranet.smith.russellmitchell.com-error.log
```

```
### intranet.smith.russellmitchell.com-error.log.1
```
[Mon Jan 24 13:01:53.940645 2022] [php7:warn] [pid 29211] [client 10.143.2.4:46358] PHP Warning:  scandir(/var/www/intranet.smith.russellmitchell.com/wp-content/uploads/wpdiscuz/cache/gravatars/): failed to open dir: No such file or directory in /var/www/intranet.smith.russellmitchell.com/wp-content
[Mon Jan 24 13:01:53.940747 2022] [php7:warn] [pid 29211] [client 10.143.2.4:46358] PHP Warning:  scandir(): (errno 2): No such file or directory in /var/www/intranet.smith.russellmitchell.com/wp-content/plugins/wpdiscuz/utils/class.WpdiscuzCache.php on line 190

```
### intranet.smith.russellmitchell.com-error.log.2
```
[Mon Jan 24 03:57:26.696483 2022] [authz_core:error] [pid 25711] [client 172.19.131.174:36072] AH01630: client denied by server configuration: /var/www/intranet.smith.russellmitchell.com/.hta
[Mon Jan 24 03:57:26.698653 2022] [authz_core:error] [pid 25711] [client 172.19.131.174:36072] AH01630: client denied by server configuration: /var/www/intranet.smith.russellmitchell.com/.hta_
[Mon Jan 24 03:57:26.700701 2022] [authz_core:error] [pid 25711] [client 172.19.131.174:36072] AH01630: client denied by server configuration: /var/www/intranet.smith.russellmitchell.com/.htaccess
```
### intranet.smith.russellmitchell.com-error.log.3
```
[Sat Jan 22 12:54:45.675233 2022] [php7:warn] [pid 19141] [client 10.143.2.4:45708] PHP Warning:  scandir(/var/www/intranet.smith.russellmitchell.com/wp-content/uploads/wpdiscuz/cache/gravatars/): failed to open dir: No such file or directory in /var/www/intranet.smith.russellmitchell.com/wp-content
[Sat Jan 22 12:54:45.675331 2022] [php7:warn] [pid 19141] [client 10.143.2.4:45708] PHP Warning:  scandir(): (errno 2): No such file or directory in /var/www/intranet.smith.russellmitchell.com/wp-content/plugins/wpdiscuz/utils/class.WpdiscuzCache.php on line 190

```
### other_vhosts_access.log
```

```

## labels (각 파일 앞 3줄)

### labels\inet-firewall\logs\dnsmasq.log
```
{"line": 1, "labels": ["dnsteal", "attacker", "dnsteal-received"], "rules": {"dnsteal": ["dnsteal.domain.match"], "attacker": ["dnsteal.domain.match"], "dnsteal-received": ["dnsteal.domain.received"]}}
{"line": 2, "labels": ["dnsteal", "attacker", "dnsteal-received"], "rules": {"dnsteal": ["dnsteal.domain.match"], "attacker": ["dnsteal.domain.match"], "dnsteal-received": ["dnsteal.domain.received"]}}
{"line": 3, "labels": ["dnsteal", "attacker", "dnsteal-received"], "rules": {"dnsteal": ["dnsteal.domain.match"], "attacker": ["dnsteal.domain.match"], "dnsteal-received": ["dnsteal.domain.received"]}}
```
### labels\internal_share\logs\audit\audit.log
```
{"line": 667, "labels": ["dnsteal", "exfiltration-service", "attacker"], "rules": {"dnsteal": ["exfil.service"], "exfiltration-service": ["exfil.service"], "attacker": ["exfil.service"]}}
{"line": 668, "labels": ["dnsteal", "exfiltration-service", "attacker"], "rules": {"dnsteal": ["exfil.service"], "exfiltration-service": ["exfil.service"], "attacker": ["exfil.service"]}}

```
### labels\intranet_server\logs\apache2\intranet.smith.russellmitchell.com-access.log.2
```
{"line": 832, "labels": ["service_scan", "foothold"], "rules": {"service_scan": ["attacker.service_scan"], "foothold": ["attacker.service_scan"]}}
{"line": 835, "labels": ["service_scan", "foothold"], "rules": {"service_scan": ["attacker.service_scan"], "foothold": ["attacker.service_scan"]}}
{"line": 836, "labels": ["attacker_http", "foothold", "service_scan"], "rules": {"attacker_http": ["attacker.foothold.apache.access"], "foothold": ["attacker.foothold.apache.access", "attacker.service_scan"], "service_scan": ["attacker.service_scan"]}}
```
### labels\intranet_server\logs\apache2\intranet.smith.russellmitchell.com-error.log.2
```
{"line": 1, "labels": ["attacker_http", "foothold", "dirb"], "rules": {"attacker_http": ["attacker.foothold.apache.error", "attacker.foothold.apache.access_error"], "foothold": ["attacker.foothold.apache.error", "attacker.foothold.apache.access_error"], "dirb": ["attacker.dirb.time"]}}
{"line": 2, "labels": ["attacker_http", "foothold", "dirb"], "rules": {"attacker_http": ["attacker.foothold.apache.error", "attacker.foothold.apache.access_error"], "foothold": ["attacker.foothold.apache.error", "attacker.foothold.apache.access_error"], "dirb": ["attacker.dirb.time"]}}
{"line": 3, "labels": ["attacker_http", "foothold", "dirb"], "rules": {"attacker_http": ["attacker.foothold.apache.error", "attacker.foothold.apache.access_error"], "foothold": ["attacker.foothold.apache.error", "attacker.foothold.apache.access_error"], "dirb": ["attacker.dirb.time"]}}
```
### labels\intranet_server\logs\audit\audit.log
```
{"line": 1860, "labels": ["attacker_change_user", "escalate"], "rules": {"attacker_change_user": ["attacker.escalate.audit.su.login"], "escalate": ["attacker.escalate.audit.su.login"]}}
{"line": 1861, "labels": ["attacker_change_user", "escalate"], "rules": {"attacker_change_user": ["attacker.escalate.audit.su.login"], "escalate": ["attacker.escalate.audit.su.login"]}}
{"line": 1862, "labels": ["attacker_change_user", "escalate"], "rules": {"attacker_change_user": ["attacker.escalate.audit.su.login"], "escalate": ["attacker.escalate.audit.su.login"]}}
```
### labels\intranet_server\logs\auth.log
```
{"line": 145, "labels": ["attacker_change_user", "escalate"], "rules": {"attacker_change_user": ["attacker.escalate.su.login"], "escalate": ["attacker.escalate.su.login"]}}
{"line": 146, "labels": ["attacker_change_user", "escalate", "escalated_command", "escalated_sudo_command"], "rules": {"attacker_change_user": ["attacker.escalate.su.login", "attacker.escalate.systemd.newsession.after"], "escalate": ["attacker.escalate.su.login", "attacker.escalate.systemd.newsessio
{"line": 147, "labels": ["attacker_change_user", "escalate"], "rules": {"attacker_change_user": ["attacker.escalate.su.login"], "escalate": ["attacker.escalate.su.login"]}}
```
### labels\vpn\logs\openvpn.log
```
{"line": 4331, "labels": ["attacker_vpn", "foothold"], "rules": {"attacker_vpn": ["attacker.foothold.vpn.ip"], "foothold": ["attacker.foothold.vpn.ip"]}}
{"line": 4332, "labels": ["attacker_vpn", "foothold"], "rules": {"attacker_vpn": ["attacker.foothold.vpn.ip"], "foothold": ["attacker.foothold.vpn.ip"]}}
{"line": 4333, "labels": ["attacker_vpn", "foothold"], "rules": {"attacker_vpn": ["attacker.foothold.vpn.ip"], "foothold": ["attacker.foothold.vpn.ip"]}}
```
