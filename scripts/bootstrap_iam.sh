#!/bin/sh

echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "🔐 Starting IAM setup..."
python3 setup_iam.py

echo "🛡️ Running CloudWatch role setup..."
python3 setup_cw_role.py

if [ $? -eq 0 ]; then
    echo "✅ IAM setup complete!"
else
    echo "❌ IAM setup failed!"
fi