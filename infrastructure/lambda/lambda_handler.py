def handler(event, context):
    print("🟢 Lambda Triggered!")
    print("📦 Event Received:", event)
    return {
        "statusCode" : 200 ,
        "body":"✅ Lambda executed successfully"
    }