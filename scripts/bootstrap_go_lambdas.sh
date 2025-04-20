#!/bin/bash

echo "🚀 Running Go Lambda bootstrap..."

# مسیر به لامبدای go
LAMBDA_DIR="init_updater"

# بررسی وجود فایل
if [ -f "$LAMBDA_DIR/build.sh" ]; then
  echo "🔧 Setting permission for build.sh..."
  chmod +x "$LAMBDA_DIR/build.sh"

  echo "🔨 Building Lambda..."
  "$LAMBDA_DIR/build.sh"

  echo "✅ Build completed."
else
  echo "❌ build.sh not found in $LAMBDA_DIR"
  exit 1
fi