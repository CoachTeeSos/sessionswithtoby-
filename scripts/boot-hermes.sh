#!/data/data/com.termux/files/usr/bin/bash
# TERMUX BOOT SCRIPT - Sessions with Toby
# Auto-starts on Termux launch

LOG="$HOME/.hermes/logs/boot.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"
}

log "=== Termux boot: starting Hermes services ==="

# 0. Acquire wake lock (prevent Android from killing Termux)
termux-wake-lock 2>/dev/null
log "Wake lock acquired"

# 1. Start WhatsApp Bridge in BOT mode (can receive messages from anyone)
BRIDGE_DIR="$HOME/.hermes/hermes-agent/scripts/whatsapp-bridge"
BRIDGE_PORT=3000

health=$(curl -s --connect-timeout 3 -o /dev/null -w "%{http_code}" http://127.0.0.1:$BRIDGE_PORT/health 2>/dev/null)
if [ "$health" != "200" ]; then
    log "Starting WhatsApp bridge in bot mode..."
    cd "$BRIDGE_DIR"
    WHATSAPP_MODE=bot node bridge.js --port $BRIDGE_PORT --session "$HOME/.hermes/whatsapp/session" --mode bot >> "$HOME/.hermes/logs/bridge.log" 2>&1 &
    sleep 5
    health=$(curl -s --connect-timeout 3 -o /dev/null -w "%{http_code}" http://127.0.0.1:$BRIDGE_PORT/health 2>/dev/null)
    if [ "$health" = "200" ]; then
        log "WhatsApp bridge started OK (bot mode)"
    else
        log "WARNING: WhatsApp bridge failed to start"
    fi
else
    log "WhatsApp bridge already running"
fi

# 2. Start Hermes Gateway
pgrep -f "hermes gateway" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    log "Starting Hermes gateway..."
    hermes gateway run >> "$HOME/.hermes/logs/gateway.log" 2>&1 &
    sleep 10
    pgrep -f "hermes gateway" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        log "Hermes gateway started OK"
    else
        log "WARNING: Hermes gateway failed to start"
    fi
else
    log "Hermes gateway already running"
fi

# 3. Start Watchdog (monitors bridge + gateway, restarts if they die)
pgrep -f "watchdog.sh" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    log "Starting watchdog..."
    bash "$HOME/.hermes/scripts/watchdog.sh" >> "$HOME/.hermes/logs/watchdog.log" 2>&1 &
    log "Watchdog started (PID: $!)"
else
    log "Watchdog already running"
fi

# 4. Run missed cron jobs (check if any jobs were missed while Termux was closed)
log "Checking for missed cron jobs..."
NOOW=$(date +%s)
# Check the last run time of the daily content job
LAST_RUN=$(python3 -c "
import json, time
try:
    with open('$HOME/.hermes/cron/jobs.json') as f:
        jobs = json.load(f)
    for j in jobs.get('jobs', []):
        if j.get('name') == 'daily-content-generation':
            last = j.get('last_run_at', 0)
            if last:
                # If last run was more than 20 hours ago, we missed it
                diff = $NOOW - last
                if diff > 72000:
                    print('MISSED')
                else:
                    print('OK')
            else:
                print('NEVER')
except:
    print('ERROR')
" 2>/dev/null)

if [ "$LAST_RUN" = "MISSED" ] || [ "$LAST_RUN" = "NEVER" ]; then
    log "Missed cron job detected - triggering daily content generation"
    # Trigger the cron job manually
    cd "$HOME/.hermes/coachtoby-site" && python3 -c "
import subprocess, os
# Run the content generation
result = subprocess.run(['python3', '$HOME/.hermes/coachtoby-site/bot/services/content_generator.py'], 
                       capture_output=True, text=True, timeout=300)
print('Content generation result:', result.returncode)
if result.stdout:
    print(result.stdout[:500])
if result.stderr:
    print('STDERR:', result.stderr[:200])
" 2>&1 | head -5 >> "$LOG"
    log "Missed content generation triggered"
else
    log "No missed cron jobs"
fi

log "=== Boot complete ==="
