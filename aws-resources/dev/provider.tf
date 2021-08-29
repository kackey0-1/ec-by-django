provider "aws" {
  region = var.AWS_REGION
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key

  // comment out if not necessary
  assume_role {
    role_arn = var.TF_ROLE
  }
}
