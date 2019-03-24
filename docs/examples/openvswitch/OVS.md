# **OpenVSwitch** Example
this document provide example of using **Pure**Flow to provisioning OpenVSwitch and configure flow inside OpenVSwitch. Before start to provisioning OpenVSwitch, please read the requirement :
- OpenVSwitch have SSH access (Using SSH public key from controller)

#### Environment
* This is environment for the example!
* OpenVSwitch is using IP Address `192.168.123.139`
* PUreFlow is using IP Address `192.168.123.24`

#### Tutorial
* This OpenVSwitch is installed on Ubuntu 16.04 (run this command on OpenVSwitch)
```
sudo apt install openvswitch-switch
```
* Add keys from PureFlow into OpenVSwitch
```
# nano .ssh/authorized_keys
```
* Make sure PureFlow devices have SSH Access (with public key) into OpenVSwitch (run this command on PureFlow)
```
ssh root@192.168.123.139
```
* Create Bridge
```
ovs-vsctl add-br br1
ovs-vsctl add-port br1 ens4
ovs-vsctl add-port br1 ens5
ovs-vsctl add-port br1 ens6
```
* Provisioning from dashboard

