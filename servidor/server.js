/**
 * K10 CHAT — SERVIDOR DE SINALIZAÇÃO PRÓPRIO
 * ============================================
 * Baseado em: PeerJS Server (peerjs npm)
 * Deploy: Render.com (gratuito) ou Railway
 *
 * COMO FUNCIONA:
 *   - Este servidor substitui o 0.peerjs.com
 *   - Só faz o handshake WebRTC (SDP + ICE) — ~1-3s por peer
 *   - Depois que peers se conectam, a comunicação é 100% P2P
 *   - Por isso, mesmo o plano gratuito suporta MILHARES de usuários/hora
 *
 * CAPACIDADE ESTIMADA (Render grátis — 512MB RAM):
 *   - ~300-600 handshakes simultâneos
 *   - Cada handshake dura ~1-3s → ~500-2000 conexões/hora
 *   - Para um chat de uso normal: suporta 1000+ usuários ativos
 */

const { PeerServer } = require('peer');
const express = require('express');

const app = express();
const PORT = process.env.PORT || 9000;

// ── Health check — necessário para o Render não "dormir" o servidor ──
app.get('/', (req, res) => {
  res.json({
    status: 'online',
    service: 'K10 Signaling Server',
    version: '1.0',
    timestamp: new Date().toISOString(),
    uptime: Math.floor(process.uptime()) + 's'
  });
});

app.get('/health', (req, res) => {
  res.json({ ok: true, peers: Object.keys(connectedPeers).length });
});

// ── Servidor de sinalização PeerJS ──────────────────────────────────
// path: '/k10' — caminho onde os peers se registram
// Muda o path e key para dificultar uso por terceiros (segurança básica)
const peerServer = PeerServer({
  port: PORT,
  path: '/k10',               // caminho do endpoint de sinalização
  key: 'k10chat',             // chave de acesso (muda se quiser mais privacidade)
  proxied: true,              // necessário para Render/Railway (proxy reverso)
  allow_discovery: false,     // desabilita listagem pública de peers (privacidade)
  
  // ── Limites de segurança ───────────────────────────────────────────
  concurrent_limit: 5000,     // máx peers simultâneos registrados
  cleanup_out_msgs: 1000,     // limpa mensagens não entregues acima de 1000
  
  // ── Alive timeout: remove peers inativos mais rápido ──────────────
  alive_timeout: 60000,       // 60s sem heartbeat → remove o peer
  expire_timeout: 5000,       // 5s para expirar mensagens pendentes
});

// ── Rastreia peers conectados para o health check ────────────────────
const connectedPeers = {};

peerServer.on('connection', (client) => {
  connectedPeers[client.getId()] = true;
  const count = Object.keys(connectedPeers).length;
  console.log(`[K10] Peer conectado: ${client.getId()} | Total: ${count}`);
  
  // Alerta de carga alta
  if (count > 400) {
    console.warn(`[K10] CARGA ALTA: ${count} peers simultâneos`);
  }
});

peerServer.on('disconnect', (client) => {
  delete connectedPeers[client.getId()];
  console.log(`[K10] Peer desconectado: ${client.getId()} | Total: ${Object.keys(connectedPeers).length}`);
});

peerServer.on('error', (err) => {
  console.error('[K10] Erro no servidor de sinalização:', err);
});

// ── Log de inicialização ─────────────────────────────────────────────
peerServer.on('mount', () => {
  console.log(`
╔══════════════════════════════════════════════════════════╗
║         K10 CHAT — SERVIDOR DE SINALIZAÇÃO               ║
║         Porta: ${PORT}                                       ║
║         Path : /k10                                      ║
║         Key  : k10chat                                   ║
╚══════════════════════════════════════════════════════════╝
  `);
});

// ── Graceful shutdown ────────────────────────────────────────────────
process.on('SIGTERM', () => {
  console.log('[K10] Encerrando servidor...');
  process.exit(0);
});
