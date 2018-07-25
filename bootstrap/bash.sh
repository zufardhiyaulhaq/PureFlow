#!/bin/bash

echo "Update the repository"
echo "============================================"
sudo apt-get -y update

echo "Install software-properties-common"
echo "============================================"
sudo apt-get install -y software-properties-common 

echo "Add Ansible Repository"
echo "============================================"
sudo apt-add-repository -y ppa:ansible/ansible

echo "Update the repository"
echo "============================================"
sudo apt-get -y update

echo "Install Ansible"
echo "============================================"
sudo apt-get install -y ansible

echo "Install requirement package"
echo "============================================"
sudo apt-get install -y wget curl nano unzip

echo "Install Java JRE"
echo "============================================"
sudo apt-get install -y default-jre

echo "Download Opendaylight"
echo "============================================"
wget https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/karaf/0.7.3/karaf-0.7.3.zip

echo "Unzip Opendaylight"
echo "============================================"
sudo mv karaf-0.7.3.zip /opt/
cd /opt/
sudo unzip karaf-0.7.3.zip

echo "Configuring Opendaylight"
echo "============================================"
cd karaf-0.7.3
sudo sh -c "echo 'feature:install odl-dlux-core odl-dluxapps-nodes odl-dluxapps-topology odl-dluxapps-applications odl-l2switch-all' >> etc/shell.init.script"

echo "Creating Daemon for Opendaylight"
echo "============================================"
sudo sh -c 'cat << EOF > /etc/systemd/system/opendaylight.service
[Unit]
Description=Opendaylight Service

[Service]
User=root
Group=root
WorkingDirectory=/opt/karaf-0.7.3/
ExecStart=/opt/karaf-0.7.3/bin/karaf

[Install]
WantedBy=multi-user.target
EOF'

echo "Starting Opendaylight as backgroud"
echo "============================================"
sudo systemctl start opendaylight
