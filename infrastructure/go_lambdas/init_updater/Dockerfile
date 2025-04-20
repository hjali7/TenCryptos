# Build stage
FROM golang:1.24.2-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN GOOS=linux GOARCH=amd64 go build -o bootstrap main.go

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/bootstrap .
COPY deploy_go_lambda.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "deploy_go_lambda.py"]