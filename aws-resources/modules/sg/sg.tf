######################
# Security Group
######################
resource "aws_security_group" "alb" {
  vpc_id = var.VPC_ID
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.DEFAULT_TAGS,
    {"Name" = "${var.ENV}-${var.PREFIX}-alb"}
  )
}

resource "aws_security_group" "django_service" {
  vpc_id = var.VPC_ID
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  tags = merge(
    var.DEFAULT_TAGS,
    {"Name" = "${var.ENV}-${var.PREFIX}-fargate-service"}
  )
}

resource "aws_security_group_rule" "allow_icmp_all" {
  type = "ingress"
  from_port = -1
  to_port   = -1
  protocol  = "icmp"
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = aws_security_group.django_service.id
}

output "alb_sg_id" {
  value = aws_security_group.alb.id
}

output "django_sg_id" {
  value = aws_security_group.django_service.id
}

