# K10 Chat — Deploy Completo

## Estrutura do pacote

```
k10-deploy/
├── servidor/          ← sobe no Render (servidor de sinalização)
│   ├── server.js
│   ├── package.json
│   └── render.yaml
├── chat/              ← seus arquivos de chat (usados após o setup)
│   ├── ServidorChatK10.html
│   ├── Chat_Desktop.HTML
│   └── K10_Monitor_Pro.html
├── setup.py           ← script de configuração automática
├── setup.bat          ← Windows: clique duplo + cole a URL
└── setup.sh           ← Mac/Linux: ./setup.sh URL
```

---

## PASSO 1 — Subir o servidor no Render (5 minutos)

1. Crie conta grátis em **https://render.com**
2. Clique **New → Web Service**
3. Escolha **"Deploy from GitHub"** (ou "Upload files")
4. Faça upload da pasta `servidor/` ou conecte ao GitHub
5. O Render detecta o `render.yaml` automaticamente
6. Clique **Deploy**
7. Aguarde ~2 minutos → aparece a URL:
   ```
   https://k10-signaling.onrender.com
   ```
   *(o nome varia — copie o que aparecer)*

---

## PASSO 2 — Configurar os arquivos de chat

### Windows
```
setup.bat k10-signaling.onrender.com
```
*(substitua pelo nome real que o Render te deu)*

### Mac / Linux
```bash
chmod +x setup.sh
./setup.sh k10-signaling.onrender.com
```

### Direto com Python (qualquer sistema)
```bash
python3 setup.py k10-signaling.onrender.com
```

**Pronto.** Os 3 arquivos em `chat/` já estão configurados.
Nenhum clique adicional. Nenhuma configuração no browser.

---

## PASSO 3 — Manter o servidor acordado (opcional, recomendado)

O Render gratuito dorme após 15 minutos sem acesso.
Para evitar:

1. Crie conta em **https://uptimerobot.com** (grátis)
2. **New Monitor → HTTP(s)**
3. URL: `https://k10-signaling.onrender.com/health`
4. Intervalo: **5 minutos**
5. Salvar

O servidor fica acordado 24/7 sem custo.

---

## Capacidade

| Plano | Handshakes/hora | Usuários simultâneos no chat |
|---|---|---|
| Render grátis | ~2.000–5.000 | Ilimitado (P2P) |
| Railway $5/mês | ~10.000+ | Ilimitado (P2P) |

> O servidor de sinalização só é usado durante 1–3 segundos por conexão.
> Depois, a comunicação é 100% P2P entre os usuários.
> Por isso um servidor gratuito aguenta milhares de usuários de chat.
