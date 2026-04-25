#!/usr/bin/env python3
"""
K10 Chat — Setup Automático
Uso: python3 setup.py <URL_DO_RENDER>
Ex:  python3 setup.py k10-signaling.onrender.com

Aplica o servidor de sinalização nos 3 arquivos HTML automaticamente.
Sem botões. Sem cliques. Sem configuração no browser.
"""

import sys, os, re

# ── Verifica argumentos ───────────────────────────────────────────────────────
if len(sys.argv) < 2:
    print("=" * 60)
    print("  K10 Chat — Configuração Automática do Servidor")
    print("=" * 60)
    print()
    print("  Uso:")
    print("    python3 setup.py <URL_DO_SEU_SERVIDOR>")
    print()
    print("  Exemplo:")
    print("    python3 setup.py k10-signaling.onrender.com")
    print()
    print("  Onde conseguir a URL:")
    print("    1. Siga o README_DEPLOY.md para criar o servidor no Render")
    print("    2. Cole a URL que o Render te deu aqui")
    print()
    sys.exit(1)

RAW_URL = sys.argv[1].strip()
# Normaliza: remove https://, http://, barras no final
SIGNAL_HOST = RAW_URL.replace("https://","").replace("http://","").rstrip("/")
SIGNAL_PATH = "/k10"
SIGNAL_KEY  = "k10chat"

print()
print("=" * 60)
print("  K10 Chat — Configuração Automática")
print("=" * 60)
print(f"  Servidor de sinalização: {SIGNAL_HOST}")
print(f"  Path:  {SIGNAL_PATH}")
print(f"  Key:   {SIGNAL_KEY}")
print("=" * 60)
print()

# Diretório dos arquivos HTML (mesma pasta do script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_DIR = os.path.join(BASE_DIR, "chat")

# ── Bloco de config a injetar no <head> ──────────────────────────────────────
# Hardcoded diretamente — zero localStorage, zero clique
HEAD_INJECT = f"""<script>
/* K10 — Servidor de sinalização configurado automaticamente */
window.K10_SIG = {{
  host: '{SIGNAL_HOST}',
  port: 443,
  secure: true,
  path: '{SIGNAL_PATH}',
  key: '{SIGNAL_KEY}'
}};
</script>
"""

# ── Patches por arquivo ───────────────────────────────────────────────────────
PATCHES = {

  "ServidorChatK10.html": [
    # Peer() principal do servidor K10
    (
      "const peer = new Peer(currentId, {\r\n          host: '0.peerjs.com',\r\n          port: 443,\r\n          secure: true,\r\n          pingInterval: 5000, // PeerJS interno: ping a cada 5s",
      "const peer = new Peer(currentId, {\r\n          ...window.K10_SIG,\r\n          pingInterval: 5000, // PeerJS interno: ping a cada 5s"
    ),
  ],

  "Chat_Desktop.HTML": [
    # 1ª instância — K10-CENTRAL (relay interno)
    (
      "      const peer = new Peer(PEER_ID, {\r\n        host: '0.peerjs.com',\r\n        port: 443,\r\n        secure: true,\r\n        debug: 0\r\n      });",
      "      const peer = new Peer(PEER_ID, { ...window.K10_SIG, debug: 0 });"
    ),
    # 2ª instância — initPeer (cliente principal)
    (
      "const peer = new Peer(peerId, {\r\nhost: '0.peerjs.com', port: 443, secure: true,",
      "const peer = new Peer(peerId, {\r\n...window.K10_SIG,"
    ),
    # 3ª instância — monitor embutido
    (
      "  peer = new Peer(id, {\r\n    host:'0.peerjs.com', port:443, secure:true, debug:0,\r\n    config:{iceServers:STUN}\r\n  });",
      "  peer = new Peer(id, { ...window.K10_SIG, debug:0, config:{iceServers:STUN} });"
    ),
  ],

  "K10_Monitor_Pro.html": [
    # Peer() do monitor
    (
      "  peer = new Peer(id, {\n    host:'0.peerjs.com', port:443, secure:true, debug:0,\n    config:{ iceServers: [{urls:'stun:stun.l.google.com:19302'},{urls:'stun:stun1.l.google.com:19302'},{urls:'stun:stun.stunprotocol.org:3478'}] }\n  });",
      f"  peer = new Peer(id, {{ ...window.K10_SIG, debug:0, config:{{ iceServers: [{{urls:'stun:stun.l.google.com:19302'}},{{urls:'stun:stun1.l.google.com:19302'}},{{urls:'stun:stun.stunprotocol.org:3478'}}] }} }});"
    ),
    # Mensagem de erro atualizada
    (
      'log("❌ Timeout de conexão PeerJS. Verifique sua conexão com 0.peerjs.com", "err");',
      f'log("❌ Timeout PeerJS. Servidor: {SIGNAL_HOST}", "err");'
    ),
  ],
}


def patch_file(filename):
    path = os.path.join(CHAT_DIR, filename)
    if not os.path.exists(path):
        print(f"  ⚠  Arquivo não encontrado: {path}")
        return False

    with open(path, "rb") as f:
        content = f.read().decode("utf-8")

    applied, failed = [], []

    for old, new in PATCHES.get(filename, []):
        if old in content:
            content = content.replace(old, new, 1)
            applied.append(old[:70].replace('\r','').replace('\n',' ').strip())
        else:
            failed.append(old[:70].replace('\r','').replace('\n',' ').strip())

    # Injeta config no <head>
    if "<head>" in content:
        content = content.replace("<head>", "<head>\n" + HEAD_INJECT, 1)
    elif re.search(r"<head\s", content):
        content = re.sub(r"(<head[^>]*>)", r"\1\n" + HEAD_INJECT, content, count=1)
    else:
        content = HEAD_INJECT + content

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    status = "✅" if not failed else "⚠️ "
    print(f"  {status} {filename}")
    for a in applied:
        print(f"       ✔  {a[:65]}")
    for ff in failed:
        print(f"       ✗  NÃO ENCONTRADO: {ff[:65]}")
    return len(failed) == 0


# ── Executa todos os patches ──────────────────────────────────────────────────
all_ok = True
for fname in ["ServidorChatK10.html", "Chat_Desktop.HTML", "K10_Monitor_Pro.html"]:
    ok = patch_file(fname)
    all_ok = all_ok and ok

print()
print("=" * 60)
if all_ok:
    print("  ✅  TUDO PRONTO!")
    print()
    print("  Os 3 arquivos em  chat/  já apontam para:")
    print(f"  → https://{SIGNAL_HOST}")
    print()
    print("  Abra normalmente:")
    print("    chat/ServidorChatK10.html  — servidor K10")
    print("    chat/Chat_Desktop.HTML     — cliente de chat")
    print("    chat/K10_Monitor_Pro.html  — monitor")
else:
    print("  ⚠️  ALGUNS PATCHES FALHARAM — veja acima")
    print("  Os arquivos que falharam ainda usam 0.peerjs.com.")
print("=" * 60)
print()
