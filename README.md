# Ghost-AD

**Active Directory Offensive Toolkit** - enumeracao, Kerberoasting, AS-REP Roasting, password spray, BloodHound-lite e hints de PTH/PTT.

```
  .-""""""""-.
 /  _       _  \
| (:3 )  (:3 )  |
|   '--------'  |
|    \ \U/ /    |
|_______________|
 \/\/\ /\ /\/\/

GHOST-AD  v1.0.0  -  Active Directory Attack Framework
By Gh0st-Bx1  |  github.com/Ghost-Bx1
```

---

## Modulos

| Subcomando | Descricao |
|---|---|
| `ldap` | Enumeracao completa via LDAP (usuarios, grupos, SPNs, AS-REP) |
| `kerb` | Kerberoasting - lista contas com SPN para crack offline |
| `asrep` | AS-REP Roasting - contas sem pre-autenticacao |
| `spray` | Password spraying com deteccao de lockout |
| `smb` | Enumeracao SMB: null session + shares |
| `bloodhound` | Coleta BloodHound-lite para JSON |
| `pth` | Hints de Pass-the-Hash / Pass-the-Ticket |

---

## Instalacao

```bash
pip install ldap3 impacket
```

> `impacket` e opcional - os modulos `spray` e `smb` degradam graciosamente e exibem comandos equivalentes com `crackmapexec` / `smbclient`.

---

## Uso

### Enumeracao LDAP

```bash
python ghost-ad.py ldap -d 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd'
python ghost-ad.py ldap -d 192.168.1.10 --domain corp.local  # sessao anonima
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

| Flag | Descricao |
|---|---|
| `-v / --verbose` | Output detalhado |
| `--output <file>` | Salva resultado em arquivo texto |

---

## Disclaimer

> **Para uso exclusivo em ambientes autorizados.** Testes de penetracao, CTF e pesquisa de seguranca ofensiva com permissao explicita do dono do ambiente. O autor nao se responsabiliza pelo uso indevido desta ferramenta.

---

**By [Gh0st-Bx1](https://github.com/Ghost-Bx1)**
