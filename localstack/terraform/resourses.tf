resource "aws_sns_topic" "sns_topic_s3_bikes_bucket_updates" {
  name = "sns_topic_s3_bikes_bucket_updates"
}

resource "aws_sqs_queue" "sqs_queue_s3_bikes_bucket_updates" {
  name = "sqs_queue_s3_bikes_bucket_updates"
}

resource "aws_sns_topic_subscription" "sub_sqs_to_updates_by_sns" {
  endpoint  = aws_sqs_queue.sqs_queue_s3_bikes_bucket_updates.arn
  protocol  = "sqs"
  topic_arn = aws_sns_topic.sns_topic_s3_bikes_bucket_updates.arn
}


resource "aws_lambda_function" "test_lambda" {
  function_name    = "test_lambda"
  filename         = data.archive_file.lambda_zip.output_path
  role             = var.lambda.role
  handler          = "test.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = var.lambda.runtime
  timeout          = var.lambda.timeout
}


