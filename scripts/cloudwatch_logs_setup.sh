#!/bin/bash

echo "📘starting cloudwatch logs setup .."

#log group
echo "📂create cloudwatch logs group"
awslocal logs create-log-group --log-group-name /aws/lambda/tencryptos-log-group

#log stream

echo "📄creating cloudwatch log stream"
awslocal logs create-log-stream --log-group-name /aws/lambda/tencryptos-log-group -log-stream-name tencryptos-log-stream

echo "✅cloudwatch logs setup complete!"