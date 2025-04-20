#!/bin/bash

echo "🔨 Building Go log analyzer lambda..."
GOOS=linux GOARCH=amd64 go build -o bootstrap main.go

echo "📦 Zipping for deployment..."
zip lambda.zip bootstrap