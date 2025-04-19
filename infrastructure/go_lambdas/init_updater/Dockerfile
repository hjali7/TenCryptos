# go_lambdas/init_updater/Dockerfile
FROM golang:1.21-alpine as builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o bootstrap main.go

# --- runtime
FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /app/bootstrap .
COPY deploy_go_lambda.py .
COPY ../../requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "deploy_go_lambda.py"]
# --- end