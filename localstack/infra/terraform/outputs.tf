output "test-sns-arn" {
  value = aws_sns_topic.sns_topic_s3_bikes_bucket_updates.arn
}