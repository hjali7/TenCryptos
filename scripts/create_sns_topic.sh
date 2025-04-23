#!/bin/bash

echo "📡 Starting SNS topic creation..."

TOPIC_NAME="tencryptos-topic"

# create topic
echo "🔧 Creating topic: $TOPIC_NAME"
TOPIC_ARN=$(awslocal sns create-topic --name "$TOPIC_NAME" --output json | jq -r .TopicArn)

# check result
if [ -n "$TOPIC_ARN" ]; then
  echo "✅ SNS topic created: $TOPIC_ARN"
else
  echo "❌ Failed to create SNS topic."
  exit 1
fi

# save ARN to a temporary file for later use (like subscribing to SQS)
echo "$TOPIC_ARN" > /tmp/sns_topic_arn.txt

echo "📦 SNS setup complete!"