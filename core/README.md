# Core Runtime - State Tracking & Communication

## Purpose
Central orchestration for the MITMonk coaching engine.
Tracks session state, manages communication loops, and coordinates between modules.

## State Management
- Session state: `vault/session-state.json`
- Metrics: `vault/metrics.json`
- Config: `config/hermes_config.yaml`

## Communication Protocol
- Output: Max compression, ultra-dense shorthand
- Format: Bullets, no filler, clinical tone
- Channel: Telegram (primary), WebUI (secondary)

## Module Coordination
```
core/pedagogy/     → NYVC framework references
core/skills/       → Automation scripts
  analytics/       → Metric scanning, trend tracking
  content/         → Content generation (human-in-the-loop)
  lead-gen/        → Lead generation scripts
core/vault/        → Session logs, metrics, DB keys
```

## Execution Rules
1. Execute existing files in `skills/` — do not spawn agents
2. Write new deterministic functions into specific directories
3. HALT after pitching topics — wait for user vector selection
4. Log all metrics to `vault/metrics.json`
5. Read history before executing — adapt to what works
