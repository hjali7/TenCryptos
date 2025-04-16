#!/bin/bash

echo "🔨 Building Go lambda for deployment..."
GOOS=linux GOARCH=amd64 go build -o bootstrap main.go

echo "📦 Packaging to lambda.zip..."
zip lambda.zip bootstrap