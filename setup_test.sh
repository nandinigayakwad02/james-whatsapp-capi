#!/bin/bash

# Quick setup script for testing

echo "🔧 Setting up .env file..."

# Create .env file with your test credentials
cat > .env << 'EOF'
# Test credentials (will replace with client's later)
META_PIXEL_ID=1554292762526086
META_ACCESS_TOKEN=PASTE_YOUR_TOKEN_HERE

# Server Configuration
PORT=8000
DEBUG=True
EOF

echo "✅ .env file created!"
echo ""
echo "⚠️  IMPORTANT: Edit .env and replace 'PASTE_YOUR_TOKEN_HERE' with the actual token from screenshot"
echo ""
echo "Then run:"
echo "  python app.py"
