#!/bin/bash

echo "Stop Service"
echo "============================================"
sudo systemctl stop dashboard
sudo systemctl stop onos
sudo systemctl disable dashboard
sudo systemctl disable onos

echo "Remove Service"
echo "============================================"
sudo rm -rf /etc/systemd/system/dashboard.service
sudo rm -rf /etc/systemd/system/onos.service

echo "Remove Data"
echo "============================================"
sudo rm -rf /opt/PureFlow
sudo rm -rf /opt/onos
sudo rm -rf /opt/onos-2.0.0.tar.gz