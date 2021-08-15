######################
# RDS
######################

resource "aws_key_pair" "instance_key" {
  key_name   = "temp_instance_key"
  public_key = file("~/.ssh/id_rsa.pub")

  tags = merge(
  var.DEFAULT_TAGS,
  {"Name": "${var.ENV}-${var.PREFIX}-key"}
  )
}

resource "aws_instance" "temp_instance" {
  ami           = "amzn-ami-hvm-2018.03.0.20190826-x86_64-gp2"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.instance_key.key_name
  vpc_security_group_ids = var.TEMP_SG_ID
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
}

#Apply scheme by using bastion host
resource "aws_db_instance" "default_bastion" {
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

  provisioner "file" {
      connection {
      user        = "ec2-user"
      host        = "bastion.example.com"
      private_key = file("~/.ssh/ec2_cert.pem")
    }


    source      = "./schema.sql"
    destination = "~"
  }

  provisioner "remote-exec" {
    connection {
      user        = "ec2-user"
      host        = "bastion.example.com"
      private_key = file("~/.ssh/ec2_cert.pem")
    }

    command = "mysql --host=${self.address} --port=${self.port} --user=${self.username} --password=${self.password} < ~/schema.sql"
  }
}
