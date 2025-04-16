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
	awsRegion := os.Getenv("AWS_REGION")
	awsEndpoint := os.Getenv("AWS_ENDPOINT")
	s3Bucket := os.Getenv("S3_BUCKET_NAME")
	sqsQueueName := os.Getenv("SQS_QUEUE_NAME")

	if awsRegion == "" || awsEndpoint == "" || s3Bucket == "" || sqsQueueName == "" {
		log.Fatal("❌ One or more required environment variables are missing.")
	}

	sess, err := session.NewSession(&aws.Config{
		Region:           aws.String(awsRegion),
		Endpoint:         aws.String(awsEndpoint),
		S3ForcePathStyle: aws.Bool(true), // لازم برای LocalStack
		Credentials:      credentials.NewStaticCredentials("test", "test", ""),
	})
	if err != nil {
		log.Fatalf("❌ AWS Session error: %v", err)
	}

	// S3
	s3Svc := s3.New(sess)
	_, err = s3Svc.CreateBucket(&s3.CreateBucketInput{
		Bucket: aws.String(s3Bucket),
	})
	if err != nil {
		fmt.Println("⚠️ S3 may already exist or failed:", err)
	} else {
		fmt.Println("✅ S3 Bucket created:", s3Bucket)
	}

	// SQS
	sqsSvc := sqs.New(sess)
	_, err = sqsSvc.CreateQueue(&sqs.CreateQueueInput{
		QueueName: aws.String(sqsQueueName),
	})
	if err != nil {
		fmt.Println("⚠️ SQS may already exist or failed:", err)
	} else {
		fmt.Println("✅ SQS Queue created:", sqsQueueName)
	}
}
