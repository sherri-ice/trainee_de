resource "aws_sns_topic" "sns_topic_s3_bikes_bucket_updates" {
  name = "sns_topic_s3_bikes_bucket_updates"
}

resource "aws_s3_bucket" "helsinki-city-bikes-bucket" {
  bucket = "helsinki-city-bikes"
}

resource "aws_s3_bucket_notification" "helsinki-city-bikes-object-created-notification" {
  bucket = aws_s3_bucket.helsinki-city-bikes-bucket.bucket
  topic {
    topic_arn     = aws_sns_topic.sns_topic_s3_bikes_bucket_updates.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "data"
    filter_suffix = ".csv"
  }
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

resource "aws_sns_topic_subscription" "sns_subscription_for_test_lambda" {
  endpoint  = aws_lambda_function.test_lambda.arn
  protocol  = "lambda"
  topic_arn = aws_sns_topic.sns_topic_s3_bikes_bucket_updates.arn
}


