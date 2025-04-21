FROM golang:1.21-alpine as builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN GOOS=linux GOARCH=amd64 go build -o bootstrap main.go

FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /app/bootstrap .
COPY deploy_log_lambda.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "deploy_log_lambda.py"]