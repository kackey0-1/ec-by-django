#!/usr/bin/env bash
# /bin/bash ~/schema.sh ${aws_db_instance.django_db.address} ${aws_db_instance.django_db.port} ${var.USERNAME} ${var.PASSWORD} ${var.APP_USER} ${var.APP_PASS}

psql --version
if [ "$?" -ne "0" ]
then
  sudo yum -y install gcc gcc-c++ kernel-devel
  sudo yum install postgresql-devel -y
  sudo yum -y install python38-devel
  sudo yum install postgresql -y
fi

export PGPASSWORD=${4}; psql --host=${1} --port=${2} --username=${3} -d template1<< EOF
CREATE DATABASE ${5} ENCODING UTF8;
CREATE USER ${5} LOGIN ENCRYPTED PASSWORD '${6}';
GRANT CONNECT ON DATABASE ${5} TO ${5};
GRANT ALL PRIVILEGES ON DATABASE ${5} TO ${5};
EOF
