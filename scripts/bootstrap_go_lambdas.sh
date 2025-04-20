#!/bin/bash

echo "🚀 Running Go Lambda deployment..."

cd /lambda || exit 1

echo "📦 Deploying Lambda..."
python3 deploy_go_lambda.py

if [ $? -eq 0 ]; then
    echo "✅ Go Lambda deployed successfully!"
else
    echo "❌ Failed to deploy Go Lambda"
fi