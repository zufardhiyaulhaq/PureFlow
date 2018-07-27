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
sudo apt-get install -y ansible crudini

echo "Configure ansible"
echo "============================================"
sudo crudini --set /etc/ansible/ansible.cfg defaults host_key_checking False

echo "Install requirement package"
echo "============================================"
sudo apt-get install -y wget curl nano unzip git python-minimal python-pip

echo "Clone Repository"
echo "============================================"
git clone https://github.com/zufardhiyaulhaq/PureFlow.git
sudo mv PureFlow/ /opt/

echo "Creating Daemon for Opendaylight"
echo "============================================"
sudo sh -c 'cat << EOF > /etc/systemd/system/dashboard.service
[Unit]
Description=Dashboard Service

[Service]
User=root
Group=root
WorkingDirectory=/opt/PureFlow/dashboard/
ExecStart=/usr/bin/python /opt/PureFlow/dashboard/dashboard.py

[Install]
WantedBy=multi-user.target
EOF'

echo "Install python dashboard requirement"
echo "============================================"
export LC_ALL=C
sudo pip install -r /opt/PureFlow/dashboard/requirement.txt

echo "Running dashboard program"
echo "============================================"
export LC_ALL=C
sudo systemctl start dashboard

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
export LC_ALL=C
sudo systemctl start opendaylight

sleep 60

sudo systemctl restart opendaylight