import boto3
import os
from dotenv import load_dotenv

# 🧪 
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# ☁️ 
AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")

# 🧑‍💼 
client = boto3.client(
    "iam",
    region_name=AWS_REGION,
    endpoint_url=AWS_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

# 🧍‍♂️ 
def create_user(user_name):
    try:
        response = client.create_user(UserName=user_name)
        print(f"✅ Created user: {user_name}")
        return response
    except client.exceptions.EntityAlreadyExistsException:
        print(f"⚠️ User already exists: {user_name}")
        return None

# 🛡️ 
def create_policy(policy_name, policy_document):
    try:
        response = client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=policy_document
        )
        print(f"✅ Created policy: {policy_name}")
        return response
    except client.exceptions.EntityAlreadyExistsException:
        print(f"⚠️ Policy already exists: {policy_name}")
        return None

# 🔗 
def attach_policy_to_user(user_name, policy_arn):
    client.attach_user_policy(
        UserName=user_name,
        PolicyArn=policy_arn
    )
    print(f"🔗 Attached policy to user: {user_name}")

# 📦 
if __name__ == "__main__":
    user_name = "devops-user"

    policy_name = "DevOpsPolicy"
    policy_doc = """{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "*",
                "Resource": "*"
            }
        ]
    }"""

    create_user(user_name)
    policy_response = create_policy(policy_name, policy_doc)

    if policy_response and "Policy" in policy_response:
        attach_policy_to_user(user_name, policy_response["Policy"]["Arn"])