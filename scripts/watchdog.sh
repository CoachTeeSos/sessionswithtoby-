#!/data/data/com.termux/files/usr/bin/bash
# WATCHDOG - Monitors WhatsApp bridge and Hermes gateway
# Restarts them if they die

LOG="$HOME/.hermes/logs/watchdog.log"
BRIDGE_PORT=3000

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"
}

log "Watchdog started"

while true; do
    # Check WhatsApp Bridge
    health=$(curl -s --connect-timeout 3 -o /dev/null -w "%{http_code}" http://127.0.0.1:$BRIDGE_PORT/health 2>/dev/null)
    if [ "$health" != "200" ]; then
        log "WhatsApp bridge DOWN (HTTP $health). Restarting..."
        pkill -f "node bridge.js" 2>/dev/null
        sleep 2
        cd "$HOME/.hermes/hermes-agent/scripts/whatsapp-bridge"
        WHATSAPP_MODE=bot node bridge.js --port $BRIDGE_PORT --session "$HOME/.hermes/whatsapp/session" --mode bot >> "$HOME/.hermes/logs/bridge.log" 2>&1 &
        sleep 5
        health=$(curl -s --connect-timeout 3 -o /dev/null -w "%{http_code}" http://127.0.0.1:$BRIDGE_PORT/health 2>/dev/null)
        if [ "$health" = "200" ]; then
            log "WhatsApp bridge restarted OK"
        else
            log "WARNING: WhatsApp bridge restart failed"
        fi
    fi

    # Check Hermes Gateway
    pgrep -f "hermes gateway" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        log "Hermes gateway DOWN. Restarting..."
        hermes gateway run >> "$HOME/.hermes/logs/gateway.log" 2>&1 &
        sleep 10
        pgrep -f "hermes gateway" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            log "Hermes gateway restarted OK"
        else
            log "WARNING: Hermes gateway restart failed"
        fi
    fi

    # Check every 60 seconds
    sleep 60
done
