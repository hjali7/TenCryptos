import json

def handler(event, context):
    print("🪂 Lambda triggered from SQS event!")
    for record in event['Records']:
        # Decode the SQS message body
        message_body = json.loads(record['body'])
        print(f"📦 Received message: {message_body}")

        # Process the message (this is where you would add your logic)
        # For example, let's just log the message
        print(f"🔍 Processing message: {message_body}")