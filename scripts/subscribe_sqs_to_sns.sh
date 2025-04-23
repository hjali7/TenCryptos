#!/bin/bash

echo "🔗 Subscribing SQS to SNS..."

TOPIC_ARN="arn:aws:sns:us-east-1:000000000000:tencryptos-topic"
QUEUE_NAME="tencryptos-queue"

# Get Queue URL
QUEUE_URL=$(awslocal sqs get-queue-url --queue-name "$QUEUE_NAME" --output text --query 'QueueUrl')

if [ -z "$QUEUE_URL" ]; then
  echo "❌ Failed to get SQS queue URL"
  exit 1
fi

# Get Queue ARN
QUEUE_ARN=$(awslocal sqs get-queue-attributes \
  --queue-url "$QUEUE_URL" \
  --attribute-name QueueArn \
  --output text --query 'Attributes.QueueArn')

if [ -z "$QUEUE_ARN" ]; then
  echo "❌ Failed to get SQS queue ARN"
  exit 1
fi

# 👇 Generate proper escaped JSON string using jq
POLICY=$(jq -c --arg QUEUE_ARN "$QUEUE_ARN" --arg TOPIC_ARN "$TOPIC_ARN" '
{
  Version: "2012-10-17",
  Statement: [
    {
      Effect: "Allow",
      Principal: "*",
      Action: "sqs:SendMessage",
      Resource: $QUEUE_ARN,
      Condition: {
        ArnEquals: {
          "aws:SourceArn": $TOPIC_ARN
        }
      }
    }
  ]
}')

# ✅ Set the policy
awslocal sqs set-queue-attributes \
  --queue-url "$QUEUE_URL" \
  --attributes "Policy=$POLICY"

# 📩 Subscribe the queue to the topic
awslocal sns subscribe \
  --topic-arn "$TOPIC_ARN" \
  --protocol sqs \
  --notification-endpoint "$QUEUE_ARN"

echo "✅ SQS subscribed to SNS!"