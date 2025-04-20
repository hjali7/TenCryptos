import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv("infrastructure/iam/.env")

iam = boto3.client(
    "iam",
    region_name=os.getenv("AWS_REGION"),
    endpoint_url=os.getenv("AWS_ENDPOINT"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# 1. ساخت Policy (اگه نباشه)
policy_name = "LambdaLogsPolicy"
policy_doc = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
            "Resource": "*"
        }
    ]
}

try:
    response = iam.create_policy(
        PolicyName=policy_name,
        PolicyDocument=json.dumps(policy_doc)
    )
    policy_arn = response["Policy"]["Arn"]
    print(f"✅ Created policy: {policy_arn}")
except iam.exceptions.EntityAlreadyExistsException:
    policy_arn = f"arn:aws:iam::000000000000:policy/{policy_name}"
    print(f"⚠️ Policy already exists: {policy_arn}")

# 2. اتصال به Role
role_name = "lambda-cw-role"
iam.attach_role_policy(
    RoleName=role_name,
    PolicyArn=policy_arn
)
print(f"🔗 Attached policy to role: {role_name}")