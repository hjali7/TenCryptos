FROM golang:1.24.2-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . ./

RUN go build -o bootstrap

FROM alpine:latest

WORKDIR /root/

COPY --from=builder /app/bootstrap .

CMD ["./bootstrap"]