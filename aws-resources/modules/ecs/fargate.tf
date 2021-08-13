
resource "aws_ecs_cluster" "main" {
  name = "django-app"
}

resource "aws_ecs_task_definition" "main" {
  family = "django_app"
  container_definitions = templatefile("definitions/ecs-task-definition.json", {
    image_uri = var.ECR_REPO_URL
  })
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  task_role_arn            = var.ECS_TASK_ROLE.arn
  execution_role_arn       = var.ECS_TASK_ROLE.arn
}

resource "aws_ecs_service" "main" {
  name    = "django_app"
  cluster = aws_ecs_cluster.main.id

  task_definition = aws_ecs_task_definition.main.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  depends_on = [var.ALB_DEPEND]

  load_balancer {
    target_group_arn = var.ALB_TARGET_GROUP.arn
    container_name   = "django_app"
    container_port   = 8000
  }

  network_configuration {
    subnets          = var.PUBLIC_SUBNETS
    security_groups  = [var.DJANGO_SG_ID]
    assign_public_ip = true
  }

  lifecycle {
    ignore_changes = [desired_count, task_definition]
  }
}

######################
# Cloudwatch
######################
resource "aws_cloudwatch_log_group" "main" {
  name = "/ecs/django_app"
}
