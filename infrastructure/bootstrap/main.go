package main

import (
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/sqs"
)

func main() {
	awsEndpoint := os.Getenv("AWS_ENDPOINT")
	region := os.Getenv("AWS_REGION")

	sess, err := session.NewSession(&aws.Config{
		Region:      aws.String(region),
		Endpoint:    aws.String(awsEndpoint),
		Credentials: credentials.NewStaticCredentials("test", "test", ""),
	})
	if err != nil {
		log.Fatalf("❌ Failed to create AWS session: %v", err)
	}

	createS3Bucket(sess)
	createSQSQueue(sess)
}

func createS3Bucket(sess *session.Session) {
	svc := s3.New(sess)
	bucket := "tencryptos-backups"

	_, err := svc.CreateBucket(&s3.CreateBucketInput{
		Bucket: aws.String(bucket),
	})
	if err != nil {
		fmt.Println("⚠️ Bucket may already exist:", err)
	} else {
		fmt.Println("✅ Created S3 bucket:", bucket)
	}
}

func createSQSQueue(sess *session.Session) {
	svc := sqs.New(sess)
	queue := "tencryptos-queue"

	_, err := svc.CreateQueue(&sqs.CreateQueueInput{
		QueueName: aws.String(queue),
	})
	if err != nil {
		fmt.Println("⚠️ Queue may already exist:", err)
	} else {
		fmt.Println("✅ Created SQS queue:", queue)
	}
}
