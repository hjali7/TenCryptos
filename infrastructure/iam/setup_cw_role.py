import boto3
import json
import os
from dotenv import load_dotenv

#🧩 loading env

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

AWS_REGION = os.getenv("AWS_REGION")
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY= os.getenv("AWS_SECRET_ACCESS_KEY")

# 🎯 static variables
ROLE_NAME = "lambda-cw-role"
ROLE_DESCRIPTION = "IAM role for Lambda function to send logs to CloudWatch"
POLICY_NAME = "lambda-basic-cw-policy"

#🛡️trust policy for run lambda
TRUST_POLICY = {
    "Version" : "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

# 📋 inline policy for access cloudWatch

LOGGING_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}

# 🛠️ create IAM client
iam = boto3.client(
    "iam",
    region_name=AWS_REGION,
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def setup_iam_role():
    # 1️⃣ create role
    try:
        iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(TRUST_POLICY),
        )
        print(f"✅ Created role: {ROLE_NAME} created.")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"⚠️ Role already exists: {ROLE_NAME}.")

    # 2️⃣add policy

    try:
        iam.put_role_policy(
            RoleName=ROLE_NAME,
            PolicyName=POLICY_NAME,
            PolicyDocument=json.dumps(LOGGING_POLICY)
        )
        print(f"✅ Policy '{POLICY_NAME}' attached to role '{ROLE_NAME}'.")
    except Exception as e:
        print(f"❌ Error attaching policy: {e}")

if __name__ == "__main__":
    setup_iam_role()
