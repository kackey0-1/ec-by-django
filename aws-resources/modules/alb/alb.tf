######################
# ALB
######################
resource "aws_alb_target_group" "main" {
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = var.VPC_ID
  target_type = "ip"

  health_check {
    path = "/login/"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_alb_listener" "main" {
  port              = "80"
  protocol          = "HTTP"
  load_balancer_arn = aws_alb.main.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.main.arn
  }
}

resource "aws_alb" "main" {
  security_groups    = [var.ALB_SG_ID]
  load_balancer_type = "application"
  subnets            = var.PUBLIC_SUBNETS
}

output "alb_depend" {
  value = aws_alb_listener.main
}

output "alb_target_group" {
  value = aws_alb_target_group.main
}
