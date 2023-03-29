data "archive_file" "lambda_zip" {
  type = "zip"
  source_file = "${var.lambda.directory}/test.py"
  output_path = "${var.lambda.directory}/test.py.zip"
}