#!/bin/sh

echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "🔐 Starting IAM setup..."
python3 setup_iam.py

echo "🎭 Setting up CloudWatch role..."
python3 setup_cw_role.py

echo "🪵 Attaching log policy to Lambda role..."
python3 attach_log_policy.py

if [ $? -eq 0 ]; then
    echo "✅ IAM full bootstrap complete!"
else
    echo "❌ IAM bootstrap failed!"
fi