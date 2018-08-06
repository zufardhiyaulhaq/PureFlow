json_data = {
    "priority": 40000,
    "isPermanent": True,
    "deviceId": None,
    "treatment": {
        "instructions": [
            {
                "type": "L2MODIFICATION",
                "subtype": "VLAN_ID",
                "vlanId": None
            },
            {
                "type": "OUTPUT",
                "port": None
            },
            {
                "type": "L2MODIFICATION",
                "subtype": "ETH_SRC",
                "mac": None
            },
            {
                "type": "L2MODIFICATION",
                "subtype": "ETH_DST",
                "mac": None
            },
            {
                "type": "L3MODIFICATION",
                "subtype": "IPV4_SRC",
                "ip": None
            },
            {
                "type": "L3MODIFICATION",
                "subtype": "IPV4_DST",
                "ip": None
            }
        ]
    },
    "selector": {
        "criteria": [
            {
                "type": "ETH_TYPE",
                "ethType": None
            },
            {
                "type": "ETH_DST",
                "mac": None
            },
            {
                "type": "ETH_SRC",
                "mac": None
            },
            {
                "type": "VLAN_VID",
                "vlanId": None
            },
            {
                "type": "IN_PORT",
                "port": None
            },
            {
                "type": "IP_PROTO",
                "protocol": None
            },
            {
                "type": "IPV4_SRC",
                "ip": None
            },
            {
                "type": "IPV4_DST",
                "ip": None
            },
            {
                "type": "TCP_SRC",
                "tcpPort": None
            },
            {
                "type": "TCP_DST",
                "tcpPort": None
            },
            {
                "type": "UDP_SRC",
                "udpPort": None
            },
            {
                "type": "UDP_DST",
                "udpPort": None
            }
        ]
    }
}

list = next((index for (index, d) in enumerate(
    json_data['treatment']['instructions']) if d["subtype"] == "VLAN_ID"), None)
print (list)
