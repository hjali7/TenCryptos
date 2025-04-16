package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

func handler(event events.SQSEvent) error {
	for _, record := range event.Records {
		fmt.Printf("📥 Received message: %s\n", record.Body)

		// 1. ارسال درخواست به بک‌اند
		url := "http://host.docker.internal:8000/cryptos/update"
		resp, err := http.Post(url, "application/json", bytes.NewBuffer([]byte("{}")))
		if err != nil {
			fmt.Println("❌ Failed to call update API:", err)
			continue
		}
		defer resp.Body.Close()
		body, _ := io.ReadAll(resp.Body)
		fmt.Println("✅ API Response:", string(body))
	}
	return nil
}

func main() {
	lambda.Start(handler)
}