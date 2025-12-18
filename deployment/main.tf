provider "aws" {
  region = "us-east-1"
}

/*
terraform destroy -target=null_resource.zip_python_script -target=null_resource.zip_python_script_name -target=aws_cloudformation_stack.config_rules_stack -auto-approve
*/
/**
resource "aws_s3_bucket_acl" "my_bucket_acl" {
  bucket = aws_s3_bucket.my_bucket.id
  acl    = "private"
}
**/
resource "aws_s3_bucket" "my_bucket" {
  bucket = "demo-python-separate-bucket-name" 
#   lifecycle {
#    prevent_destroy = true
#  }
}

resource "null_resource" "zip_python_script" {
  provisioner "local-exec" {
    #command = "zip -j ${path.module}/Child-Script/index.zip ${path.module}/Child-Script/index.py" 
    command = "zip -j ${path.module}/Child-Script/CSV_Script.zip ${path.module}/Child-Script/CSV_Script.py" 
  }
}

resource "null_resource" "zip_python_script_name" {
  provisioner "local-exec" {
    #command = "zip -j ${path.module}/Child-Script/index.zip ${path.module}/Child-Script/index.py" 
    command = "zip -j ${path.module}/Child-Script/Rule_Name_Check_Script.zip ${path.module}/Child-Script/Rule_Name_Check_Script.py" 

  }
}

resource "aws_s3_object" "my_script_zip" {
  bucket = aws_s3_bucket.my_bucket.bucket
  #key    = "index.zip" 
  #source = "${path.module}/Child-Script/index.zip"
  key    = "CSV_Script.zip" 
  source = "${path.module}/deployment/Child-Script/CSV_Script.zip"
  acl    = "private"

  depends_on = [null_resource.zip_python_script]
}

resource "aws_s3_object" "my_script_zip_name" {
  bucket = aws_s3_bucket.my_bucket.bucket
  #key    = "index.zip" 
  #source = "${path.module}/Child-Script/index.zip"
  key    = "Rule_Name_Check_Script.zip" 
  source = "${path.module}/deployment/Child-Script/Rule_Name_Check_Script.zip"
  acl    = "private"

  depends_on = [null_resource.zip_python_script_name]
}

resource "aws_cloudformation_stack" "config_rules_stack" {
  name          = "ConfigRulesStack"
  template_body = file("${path.module}/Child-CFT/Combine-config-rules.yaml")
  capabilities = ["CAPABILITY_IAM"]
}

# Invoke Lambda Function after deployment
data "aws_lambda_invocation" "invoke_lambda" {
  function_name = aws_cloudformation_stack.config_rules_stack.outputs["ConfigRuleLambdaFunction"]
  input         = jsonencode({})
}

# Output the Lambda function response
output "lambda_response" {
  value = data.aws_lambda_invocation.invoke_lambda.result
}
