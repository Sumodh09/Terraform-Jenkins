resource "aws_cloudformation_stack" "child_cft" {
  name         = "Child-CFT-Deployment"
  template_body = file("Child-CFT/demo-cft.yaml")

  capabilities = ["CAPABILITY_NAMED_IAM"]
}
