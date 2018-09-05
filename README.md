# **Pure**Flow

PureFlow is platform that can provisioning device to connect to openflow controller and modify flow inside the device via controller API. This platform is open to contribute.

---
## **Device Support**
---
This is are list of supported devices :
- OpenVSwitch
- MikroTik

## **Feature**
---
PureFlow Feature :
- Support OpenFlow 1.0 & 1.3 (tested)
- View Flow
- Config Flow

Future Works :
- More Devices Support
- Bulk Provisioning
- Improvement in dashboard & database system

## **Architecture**
---
PureFlow using Ansible and ONOS as main Backend tools. Ansible is use to provisioning the devices via SSH and ONOS to control, modify & view the flow inside devices.

<span style="display:block;text-align:center">![architecture](https://raw.githubusercontent.com/zufardhiyaulhaq/PureFlow/master/assets/architecture.png)</span>

## **Flow**
---
For provisioning devices, its use Ansible SSH based method to configure devices. For controlling the flow inside the devices, you can use web dashboard that communicate with ONOS controller.
<span style="display:block;text-align:center">![provisioning](https://raw.githubusercontent.com/zufardhiyaulhaq/PureFlow/master/assets/provisioning.png)</span>

## **Instalation**
For instalation procedure, go to docs directory on this repository

## **Secrenshot**
<span style="display:block;text-align:center">![screenshoot](https://raw.githubusercontent.com/zufardhiyaulhaq/PureFlow/master/assets/pureflow1.png)</span>
<span style="display:block;text-align:center">![screenshoot](https://raw.githubusercontent.com/zufardhiyaulhaq/PureFlow/master/assets/pureflow2.png)</span>
<span style="display:block;text-align:center">![screenshoot](https://raw.githubusercontent.com/zufardhiyaulhaq/PureFlow/master/assets/pureflow3.png)</span>
<span style="display:block;text-align:center">![screenshoot](https://raw.githubusercontent.com/zufardhiyaulhaq/PureFlow/master/assets/pureflow4.png)</span>
<span style="display:block;text-align:center">![screenshoot](https://raw.githubusercontent.com/zufardhiyaulhaq/PureFlow/master/assets/pureflow5.png)</span>
<span style="display:block;text-align:center">![screenshoot](https://raw.githubusercontent.com/zufardhiyaulhaq/PureFlow/master/assets/pureflow6.png)</span>
<span style="display:block;text-align:center">![screenshoot](https://raw.githubusercontent.com/zufardhiyaulhaq/PureFlow/master/assets/pureflow7.png)</span>
<span style="display:block;text-align:center">![screenshoot](https://raw.githubusercontent.com/zufardhiyaulhaq/PureFlow/master/assets/pureflow8.png)</span>