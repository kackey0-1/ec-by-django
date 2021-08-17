######################
# RDS
######################
resource "aws_rds_cluster" "django_db" {
  cluster_identifier      = "aurora-cluster-django-db"
  engine                  = "aurora-postgresql"


  database_name           = "django_db"
  master_username         = var.USERNAME
  master_password         = var.PASSWORD

  db_subnet_group_name    = var.DB_SUBNET_GROUP
  vpc_security_group_ids  = [var.DB_SG_ID]

  skip_final_snapshot  = true

  tags = merge(
    var.DEFAULT_TAGS,
    { "Name": "${var.ENV}-${var.PREFIX}-db-cluster" }
  )
}

resource "aws_rds_cluster_instance" "cluster_instances" {
  count              = 1
  identifier         = "aurora-cluster-django-db-${count.index}"
  cluster_identifier = aws_rds_cluster.django_db.id
  instance_class     = "db.t3.medium"
  engine             = aws_rds_cluster.django_db.engine
}

resource "aws_rds_cluster_endpoint" "django_db_rw" {
  cluster_identifier          = aws_rds_cluster.django_db.id
  cluster_endpoint_identifier = "rw"
  custom_endpoint_type        = "ANY"
}

resource "aws_rds_cluster_endpoint" "django_db_ro" {
  cluster_identifier          = aws_rds_cluster.django_db.id
  cluster_endpoint_identifier = "ro"
  custom_endpoint_type        = "READER"
}

resource "aws_key_pair" "instance_key" {
  key_name   = "temp_instance_key"
  public_key = file("~/.ssh/id_rsa.pub")

  tags = merge(
  var.DEFAULT_TAGS,
  {"Name": "${var.ENV}-${var.PREFIX}-key"}
  )
}

resource "aws_instance" "temp_instance" {
  ami           = "ami-0ab3e16f9c414dee7"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.instance_key.key_name
  vpc_security_group_ids = [var.TEMP_SG_ID]
  subnet_id = var.PUBLIC_SUBNETS[0]

  root_block_device {
    volume_type = "gp2"
    volume_size = 10
  }

  tags = merge(
    var.DEFAULT_TAGS,
    {"Name": "${var.ENV}-${var.PREFIX}-temp"}
  )

  lifecycle { create_before_destroy = true }


  provisioner "file" {
    connection {
      user        = "ec2-user"
      host        = aws_instance.temp_instance.public_ip
      private_key = file("~/.ssh/id_rsa")
    }

    source      = "../scripts/schema.sh"
    destination = "/home/ec2-user/schema.sh"
  }

  provisioner "remote-exec" {
    connection {
      user        = "ec2-user"
      host        = aws_instance.temp_instance.public_ip
      private_key = file("~/.ssh/id_rsa")
    }

    inline = [
      "/bin/bash ~/schema.sh ${aws_rds_cluster_endpoint.django_db_rw.endpoint} ${aws_rds_cluster.django_db.port} ${var.USERNAME} ${var.PASSWORD} ${var.APP_USER} ${var.APP_PASS}"
    ]
  }
  depends_on = [aws_rds_cluster_instance.cluster_instances]
}
