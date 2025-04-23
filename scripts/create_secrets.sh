#!/bin/bash

echo "🔐 Creating Secrets in Secrets Manager..."

# create DB pass secret

awslocal secretsmanager create-secret --name db-password --secret-string "devpass123"

echo "✅ Secrets created!"