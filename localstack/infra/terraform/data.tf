data "local_file" "lambda_load_data_to_dynamodb_zip" {
  filename    = "${path.module}/../../lambda/zip/lambda_load_data_to_dynamodb.py.zip"
}

data aws_iam_policy_document lambda_assume_role {
  statement {
    actions = ["sts:AssumeRole"]
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data aws_iam_policy_document lambda_s3 {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:GetObjectAttributes"
    ]

    resources = [
      "arn:aws:s3:::${aws_s3_bucket.helsinki-city-bikes-bucket.bucket}/*"
    ]
  }
}