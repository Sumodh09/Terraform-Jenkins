provider "aws" {
  region = "us-east-1"
}


resource "aws_cloudformation_stack" "child_cft" {
  name         = "Child-CFT-Deployment"
  template_body = file("Child-CFT/CFT-Manage-rule.yaml")

  capabilities = ["CAPABILITY_NAMED_IAM"]
}
