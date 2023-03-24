variable "aws" {
  type = object({
    access_key = string
    secret_key = string
    region     = string
  })
  default = {
    access_key = "test_access_key"
    secret_key = "test_secret_key"
    region     = "eu-north-1"
  }
}