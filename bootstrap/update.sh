echo "Update Program"
echo "============================================"
cd /opt/PureFlow/
sudo git pull

echo "Restart service"
echo "============================================"
sudo systemctl restart dashboard