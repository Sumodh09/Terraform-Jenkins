locals {
  s3_config_rules = {
    s3-bucket-public-read-prohibited = {
      identifier = "S3_BUCKET_PUBLIC_READ_PROHIBITED"
      types      = ["AWS::S3::Bucket"]
    }
    s3-bucket-ssl-requests-only = {
      identifier = "S3_BUCKET_SSL_REQUESTS_ONLY"
      types      = ["AWS::S3::Bucket"]
    }
    s3-bucket-logging-enabled = {
      identifier = "S3_BUCKET_LOGGING_ENABLED"
      types      = ["AWS::S3::Bucket"]
    }
  }
}

resource "aws_config_config_rule" "s3_rules" {
  for_each = local.s3_config_rules

  name = each.key

  source {
    owner             = "AWS"
    source_identifier = each.value.identifier
  }

  scope {
    compliance_resource_types = each.value.types
  }
}
