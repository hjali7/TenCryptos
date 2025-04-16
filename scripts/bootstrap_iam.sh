#!/bin/bash

echo "📦 Installing Python dependencies..."
pip install --no-cache-dir -r ./infrastructure/requirements.txt

echo "🔐 Starting IAM setup..."
python3 ./infrastructure/iam/setup_iam.py

if [ $? -eq 0 ]; then
    echo "✅ IAM setup complete!"
else
    echo "❌ IAM setup failed!"
fi