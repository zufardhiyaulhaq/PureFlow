#!/bin/bash
echo "Update the repository"
echo "============================================"
sudo apt-get -y update

echo "Install mysql"
echo "============================================"
sudo apt-get -y install mysql-server libmysqlclient-dev

echo "Bootstraping mysql database"
echo "============================================"
DATABASE="pureflow"
USERDB="pureflowadmin"
PASSWDDB="pureflowpassword"

echo "Please enter root user MySQL password!"
echo "============================================"
read rootpasswd

echo "Creating Databases"
echo "============================================"
mysql -uroot -p${rootpasswd} -e "CREATE DATABASE ${DATABASE};"
mysql -uroot -p${rootpasswd} -e "CREATE USER '${USERDB}'@'%' IDENTIFIED BY '${PASSWDDB}';"
mysql -uroot -p${rootpasswd} -e "GRANT ALL PRIVILEGES ON ${DATABASE} . * TO '${USERDB}'@'%';"
mysql -uroot -p${rootpasswd} -e "SHOW GRANTS FOR '${USERDB}'@'%';"
mysql -uroot -p${rootpasswd} -e "FLUSH PRIVILEGES;"

echo "Import Databases"
echo "============================================"
mysql -u${USERDB} -p${PASSWDDB} ${DATABASE} < pureflow.sql


