FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY deploy_lambda.py .
COPY lambda_handler.py .
COPY .env .

CMD ["python3", "deploy_lambda.py"]