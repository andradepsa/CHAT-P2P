const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Servir arquivos estáticos da pasta atual
app.use(express.static(__dirname));

// Rota principal - entrega o index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Rota de ping (para verificação manual ou por serviços externos)
app.get('/ping', (req, res) => {
  res.status(200).send('pong');
});

// Rota de health check (opcional, para monitoramento)
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Função de auto-ping para evitar hibernação no Render
function selfPing() {
  // O Render injeta automaticamente a variável RENDER_EXTERNAL_URL
  const publicUrl = process.env.RENDER_EXTERNAL_URL;
  
  if (!publicUrl) {
    // Se não estiver no Render (ex: ambiente local), apenas loga e não faz ping
    console.log('[AUTO-PING] Ambiente local ou variável não definida. Ignorando.');
    return;
  }

  const pingUrl = `${publicUrl}/ping`;
  
  fetch(pingUrl)
    .then(res => {
      if (res.ok) {
        console.log(`[AUTO-PING] ✅ ${new Date().toISOString()} - Servidor ativo (${res.status})`);
      } else {
        console.warn(`[AUTO-PING] ⚠️ ${new Date().toISOString()} - Resposta inesperada: ${res.status}`);
      }
    })
    .catch(err => {
      console.error(`[AUTO-PING] ❌ ${new Date().toISOString()} - Erro: ${err.message}`);
    });
}

// Configurar o auto-ping: a cada 10 minutos (600.000 ms)
// Isso garante que o servidor nunca fique 15 minutos sem tráfego
const PING_INTERVAL_MS = 10 * 60 * 1000; // 10 minutos

// Inicia o ping periódico
setInterval(selfPing, PING_INTERVAL_MS);

// Também faz um ping inicial após 30 segundos (para garantir que comece logo)
setTimeout(selfPing, 30 * 1000);

// Inicia o servidor
app.listen(port, '0.0.0.0', () => {
  console.log(`🚀 Servidor K10 rodando em http://0.0.0.0:${port}`);
  console.log(`📡 Modo: ${process.env.RENDER_EXTERNAL_URL ? 'Render (auto-ping ativo)' : 'Local/desenvolvimento'}`);
  if (process.env.RENDER_EXTERNAL_URL) {
    console.log(`🔗 URL pública: ${process.env.RENDER_EXTERNAL_URL}`);
    console.log(`⏰ Auto-ping a cada ${PING_INTERVAL_MS / 60000} minutos para evitar hibernação`);
  }
});
