package main

import (
    "context"
    "encoding/json"
    "fmt"
    "strings"

    "github.com/aws/aws-lambda-go/events"
    "github.com/aws/aws-lambda-go/lambda"
    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/sqs"
    "os"
)

var (
	sqsClient *sqs.SQS
	queueURL = os.Getenv("SQS_QUEUE_URL")
)

func init() {
	sess := session.Must(session.NewSession(&aws.Config{
		Region: aws.String(os.Getenv("AWS_REGION")),
		Endpoint: aws.String(os.Getenv("SQS_ENDPOINT")),
		CredentialsChainVerboseErrors: aws.Bool(true),
	}))
	sqsClient = sqs.New(sess)
}

func handler(ctx context.Context, event events.CloudwatchLogsEvent) error {
    logs, err := event.AWSLogs.Parse()
    if err != nil {
        return fmt.Errorf("parse logs error: %v", err)
    }

    for _, logEvent := range logs.LogEvents {
        if strings.Contains(strings.ToLower(logEvent.Message), "error") {
            msgBody, _ := json.Marshal(logEvent)
            _, err := sqsClient.SendMessage(&sqs.SendMessageInput{
                QueueUrl:    aws.String(queueURL),
                MessageBody: aws.String(string(msgBody)),
            })
            if err != nil {
                return fmt.Errorf("send to SQS error: %v", err)
            }
        }
    }

    return nil
}

func main() {
    lambda.Start(handler)
}