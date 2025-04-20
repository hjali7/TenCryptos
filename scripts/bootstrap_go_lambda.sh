#!/bin/bash

echo "🚀 Running Go Lambda bootstrap..."

cd /lambda || exit 1

echo "🔨 Building Go Lambda..."
chmod +x ./build.sh
./build.sh

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "📦 Deploying Lambda..."
python3 deploy_go_lambda.py

if [ $? -eq 0 ]; then
    echo "✅ Go Lambda deployed successfully!"
else
    echo "❌ Failed to deploy Go Lambda"
fi