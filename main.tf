provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "etl_bucket" {
  bucket = var.s3_bucket_name

  tags = {
    Name        = "ETL S3 Bucket"
    Environment = "Development"
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "etl_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name   = "etl_lambda_policy"
  role   = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["s3:*"]
        Effect   = "Allow"
        Resource = ["${aws_s3_bucket.etl_bucket.arn}/*"]
      },
      {
        Action   = ["logs:*"]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_lambda_function" "etl_lambda" {
  function_name = "ETLFunction"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"

  s3_bucket = aws_s3_bucket.etl_bucket.id
  s3_key    = "lambda_code.zip"

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.etl_bucket.bucket
    }
  }

  timeout     = 15
  memory_size = 128

  

  depends_on = [aws_iam_role_policy.lambda_policy]
  
  provisioner "local-exec" {
    command = <<EOT
      aws lambda invoke \
        --function-name ${self.function_name} \
        --payload '{"test": "trigger"}' \
        output.json
    EOT
  }
}

resource "aws_s3_object" "lambda_code" {
  bucket = aws_s3_bucket.etl_bucket.id
  key    = "lambda_code.zip"
  source = "lambda_code.zip"
}



