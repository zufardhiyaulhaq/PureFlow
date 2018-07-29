# Install

This document provide instalation of **Pure**Flow. You need Ubuntu 16.04 to install the **Pure**Flow. Just clone the repository
```
git clone https://github.com/zufardhiyaulhaq/PureFlow.git
```
go to bootstrap folder and running the bash script
```
cd Pureflow/bootstrap
sh install.sh
```
this script will install all of **Pure**Flow files inside `/opt`

## Post Install
---
You maybe need to generate SSH public key inside **Pure**Flow to configure the devices
```
sudo su
ssh-keygen
```
your `public-key` have address in
```
/root/.ssh/id-rsa.pub
```

## Update
---
When there are some update on dashboard side, just running the bash script
```
cd Pureflow/bootstrap
sh update.sh
```
this script will pull the latest version dashboard and restart the dashboard.

## Uninstall
---
To uninstall **Pure**Flow, basically just running the bash script
```
cd Pureflow/bootstrap
sh remove.sh
```

