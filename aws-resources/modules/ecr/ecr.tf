######################
# ECR
######################
resource "aws_ecr_repository" "main" {
  name = "django_app"
}

output "ecr_repository_url" {
  value = aws_ecr_repository.main.repository_url
}