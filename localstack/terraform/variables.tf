variable "aws" {
  type = object({
    access_key = string
    secret_key = string
    region     = string
    endpoint   = map(string)
  })
  default = {
    access_key = "mock_access_key"
    secret_key = "mock_secret_key"
    region     = "us-east-1"
    endpoint   = {
      dynamodb = "http://localhost:4566"
      iam      = "http://localhost:4566"
      lambda   = "http://localhost:4566"
      s3       = "http://localhost:4566"
      sns      = "http://localhost:4566"
      sqs      = "http://localhost:4566"
    }
  }
}

variable "lambda" {
  type = object({
    directory = string
    role = string
    runtime = string
    timeout = number
  })
  default = {
    directory = "../lambda"
    role = "mock_role"
    runtime = "python3.9"
    timeout = 900
  }
}
