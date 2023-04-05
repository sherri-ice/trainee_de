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
      lambda   = "http://localhost:4566"
      s3       = "http://localhost:4566"
      sns      = "http://localhost:4566"
    }
  }
}

variable "dynamodb" {
  type = object({
    capacity = map(number)
  })
  default = {
    capacity = {
      read  = 10
      write = 10
    }
  }
}

variable "lambda" {
  type = object({
    source_dir = string
    zip_dir = string
    role = string
    runtime = string
    timeout = number
  })
  default = {
    source_dir = "../../lambda/source"
    zip_dir = "../../lambda/zip"
    role = "mock_role"
    runtime = "python3.9"
    timeout = 900
  }
}
