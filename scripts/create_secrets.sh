#!/bin/bash

echo "🔐 Creating Secrets in Secrets Manager..."

# create DB pass secret

awslocal secretsmanager create-secret --name db-password --secret-string "devpass123"
awslocal secretsmanager create-secret --name s3-bucket-name --secret-string "tencryptos-backups"
awslocal secretsmanager create-secret --name sqs-queue-url --secret-string "http://172.19.0.2:4566/000000000000/tencryptos-queue"

echo "✅ Secrets created!"