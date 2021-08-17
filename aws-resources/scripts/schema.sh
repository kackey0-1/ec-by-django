mysql --version
if [ "$?" -ne "0" ]
then
    sudo yum update -y
    sudo yum install mysql -y
fi

mysql --host=${1} --port=${2} --user=${3} --password=${4}  << EOF
CREATE DATABASE ${5} CHARACTER SET UTF8mb4;
CREATE USER '${5}' IDENTIFIED BY '${6}';
GRANT ALL PRIVILEGES ON ${5}.* TO '${5}';
EOF