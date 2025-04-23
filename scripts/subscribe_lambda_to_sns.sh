#!/bin/bash

echo "🔔 Subscribing Lambda to SNS..."


TOPIC_NAME="tencryptos-topic"
FUNCTION_NAME="GoInitUpdater"

TOPIC_ARN="arn:aws:sns:us-east-1:000000000000:$TOPIC_NAME"
LAMBDA_ARN="arn:aws:lambda:us-east-1:000000000000:function:$FUNCTION_NAME"

awslocal lambda add-permission \
  --function-name "$FUNCTION_NAME" \
  --statement-id sns-invoke-lambda \
  --action "lambda:InvokeFunction" \
  --principal sns.amazonaws.com \
  --source-arn "$TOPIC_ARN" \
  >/dev/null && echo "✅ Lambda permission granted." || echo "⚠️ Permission may already exist."

awslocal sns subscribe \
  --topic-arn "$TOPIC_ARN" \
  --protocol lambda \
  --notification-endpoint "$LAMBDA_ARN"

echo "✅ Lambda subscribed to SNS successfully!"