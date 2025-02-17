provider "aws" {
  region = "us-east-1"
  access_key = "AKIA2HEQVMFDAYZEM63W"
  secret_key = "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"
}

resource "aws_cloudformation_stack" "child_cft" {
  name         = "Child-CFT-Deployment"
  template_body = file("Child-CFT/demo-cft.yaml")

  capabilities = ["CAPABILITY_NAMED_IAM"]
}
