#!/bin/bash

echo "🔥 LIVE WEBHOOK MONITOR"
echo "======================================"
echo "Watching: http://localhost:8000/webhook"
echo "Press Ctrl+C to stop"
echo "======================================"
echo ""

# Watch server logs in real-time
tail -f /tmp/manychat_webhook.log 2>/dev/null || echo "Waiting for first webhook..."
