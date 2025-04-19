# lambda/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ../../requirements.txt ./requirements.txt
COPY lambda_handler.py .
COPY deploy_lambda.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "deploy_lambda.py"]
