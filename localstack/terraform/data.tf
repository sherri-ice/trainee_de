data "archive_file" "lambda_zip" {
  type = "zip"
  source_dir = var.lambda.source_dir
  output_path = "${var.lambda.zip_dir}/test.py.zip"
}