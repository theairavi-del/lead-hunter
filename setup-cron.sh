#!/bin/bash
# Setup cron job for 30-minute lead updates
# Run this script once to enable automation

echo "🔧 Setting up Lead Hunter automation..."
echo ""

# Get the directory
DIR="$HOME/.openclaw/workspace/lead-hunter"

# Create cron entry (runs every 30 minutes)
CRON_ENTRY="*/30 * * * * cd $DIR && /usr/bin/python3 lead_hunter_demo.py >> cron.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ Cron job added!"
echo ""
echo "📋 Schedule: Every 30 minutes"
echo "📁 Location: $DIR"
echo "📊 Logs: $DIR/cron.log"
echo ""
echo "To verify:"
echo "  crontab -l"
echo ""
echo "To remove:"
echo "  crontab -e  (delete the line)"
echo ""
echo "🚀 Your dashboard will auto-update at:"
echo "   https://theairavi-del.github.io/lead-hunter/"