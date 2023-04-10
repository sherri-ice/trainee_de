resource "aws_sns_topic" "sns_topic_s3_bikes_bucket_updates" {
  name = "sns_topic_s3_bikes_bucket_updates"
}

resource "aws_s3_bucket" "helsinki-city-bikes-bucket" {
  bucket = "helsinki-city-bikes"
}

resource "aws_dynamodb_table" "helsinki-city-bikes-raw-table" {
  name           = "helsinki_city_bikes_raw"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "departure_id"
  range_key      = "return_id"
  attribute {
    name = "departure_id"
    type = "N"
  }
  attribute {
    name = "return_id"
    type = "N"
  }
}

resource "aws_dynamodb_table" "helsinki-city-bikes-station_metrics-table" {
  name           = "helsinki_city_bikes_station_metrics"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "station_name"
  attribute {
    name = "station_name"
    type = "S"
  }
}

resource "aws_dynamodb_table" "helsinki-city-bikes-daily-metrics-table" {
  name           = "helsinki_city_bikes_daily_metrics"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "date"
  attribute {
    name = "date"
    type = "S"
  }
}

resource "aws_dynamodb_table" "helsinki-city-bikes-monthly-metrics-table" {
  name           = "helsinki_city_bikes_monthly_metrics"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "date"
  attribute {
    name = "date"
    type = "S"
  }
}

resource "aws_s3_bucket_notification" "helsinki-city-bikes-object-created-notification" {
  bucket = aws_s3_bucket.helsinki-city-bikes-bucket.bucket
  topic {
    topic_arn     = aws_sns_topic.sns_topic_s3_bikes_bucket_updates.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "data"
    filter_suffix = ".csv"
  }

  topic {
    topic_arn     = aws_sns_topic.sns_topic_s3_bikes_bucket_updates.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "metrics"
    filter_suffix = ".csv"
  }
}

resource aws_iam_policy lambda_s3 {
  name        = "lambda-s3-permissions"
  description = "Contains S3 read permission for lambda"
  policy      = data.aws_iam_policy_document.lambda_s3.json
}

resource aws_iam_role lambda_role {
  name               = "lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource aws_iam_role_policy_attachment lambda_s3 {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_s3.arn
}

resource "aws_lambda_function" "lambda_load_data_to_dynamodb" {
  function_name    = "lambda_load_data_to_dynamodb"
  filename         = data.local_file.lambda_load_data_to_dynamodb_zip.filename
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_load_data_to_dynamodb.lambda_handler"
  runtime          = var.lambda.runtime
  timeout          = var.lambda.timeout
  source_code_hash = data.local_file.lambda_load_data_to_dynamodb_zip.content_base64
  environment {
    variables = {
      AWS_ACCESS_KEY   = var.aws.access_key
      AWS_SECRET_KEY   = var.aws.secret_key
      AWS_REGION_NAME  = var.aws.region
    }
  }
}

resource "aws_sns_topic_subscription" "sns_subscription_for_test_lambda" {
  endpoint  = aws_lambda_function.lambda_load_data_to_dynamodb.arn
  protocol  = "lambda"
  topic_arn = aws_sns_topic.sns_topic_s3_bikes_bucket_updates.arn
}


