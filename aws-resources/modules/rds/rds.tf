######################
# RDS
######################
resource "aws_db_instance" "django_db" {
  identifier           = "${var.ENV}${var.PREFIX}"
  allocated_storage    = 5
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  username             = var.USERNAME
  password             = var.PASSWORD
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
  vpc_security_group_ids = [var.DB_SG_ID]
  db_subnet_group_name = var.DB_SUBNET_GROUP

  tags = merge(
    var.DEFAULT_TAGS,
    { "Name": "${var.ENV}-${var.PREFIX}-db" }
  )
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
      "/bin/bash ~/schema.sh ${aws_db_instance.django_db.address} ${aws_db_instance.django_db.port} ${var.USERNAME} ${var.PASSWORD} ${var.APP_USER} ${var.APP_PASS}"
    ]
  }
}
