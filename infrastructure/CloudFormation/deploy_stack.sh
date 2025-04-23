#!/bin/bash

set -e  # اگر خطایی پیش اومد، اسکریپت متوقف بشه
echo "🚀 Starting full TenCryptos deployment stack..."

# 1. Set script permissions
echo "🔐 Setting permissions for scripts..."
chmod +x scripts/*.sh || true
echo "✅ Permissions set."

# 2. Start LocalStack
echo "🟢 Bringing up LocalStack..."
make localstack-up

# 3. Start the main project stack
echo "📦 Starting TenCryptos services..."
make up

# 4. Optional bootstrap: CloudWatch logs, Lambda deployment, etc.
echo "🔧 Running cloudwatch log setup..."
make cloudwatch-logs

echo "⚙️ Running go-lambda-updater..."
make go-lambda-updater

# 5. Final status
echo "✅ All services deployed successfully!"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
