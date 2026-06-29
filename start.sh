#!/bin/bash
set -e
export HERMES_HOME=/opt/data
export HERMES_WRITE_SAFE_ROOT=/opt/data
export WHATSAPP_MODE=bot
mkdir -p /opt/data/logs

if [ -d /opt/data/whatsapp/session ] && [ "$(ls -A /opt/data/whatsapp/session 2>/dev/null)" ]; then
    echo "[$(date)] WhatsApp session found"
else
    echo "[$(date)] WARNING: No WhatsApp session - copy from Termux or pair interactively"
fi

cd /opt/hermes
node /opt/hermes/hermes-agent/scripts/whatsapp-bridge/bridge.js --port 3000 --session /opt/data/whatsapp/session --mode bot >> /opt/data/logs/bridge.log 2>&1 &
echo "[$(date)] WhatsApp bridge started (PID: $!)"

for i in $(seq 1 15); do
    curl -s http://localhost:3000/health > /dev/null 2>&1 && echo "[$(date)] WhatsApp bridge ready!" && break
    sleep 2
done

echo "[$(date)] Starting Hermes Gateway..."
hermes gateway run >> /opt/data/logs/gateway.log 2>&1 &
echo "[$(date)] Gateway started (PID: $!)"

for i in $(seq 1 30); do
    curl -s http://localhost:8080/health > /dev/null 2>&1 && echo "[$(date)] Gateway ready!" && break
    sleep 2
done

echo "[$(date)] All services running..."
wait
