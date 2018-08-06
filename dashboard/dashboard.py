from flask import Flask, render_template, session, redirect, flash
from flask import request

import os
import ast
import json
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

def search(dict, key, value):
    for i, j in enumerate(dict):
        try:
            j[key]
        except KeyError:
            print ('error')
        else:
            if j[key] == value:
                return i
                break

def get(append):
    url = 'http://127.0.0.1:8181/onos/v1'+append
    data = requests.get(url, auth=HTTPBasicAuth(
        'onos', 'rocks')).text.decode('utf-8')
    return json.loads(data)


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect("/")


@app.route('/login', methods=['POST'])
def admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return redirect("/")


@app.route('/configuring')
def configuring():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        data = get("/devices")
        return render_template('configuring.html', data=data)


@app.route('/configuring/api', methods=['POST', 'GET'])
def device():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        raw = request.form.to_dict(flat=True)
        data = {k.encode('utf8'): v.encode('utf8') for k, v in raw.items()}
        return render_template('configuring-device.html', data=data)


@app.route('/configuring/controller', methods=['POST'])
def configuring_api():
    raw = request.form.to_dict(flat=True)
    res = {k.encode('utf8'): v.encode('utf8') for k, v in raw.items()}
    data = dict((k, v) for k, v in res.iteritems() if v)
    # Priority, Permanent, is not defined in form, so we defined inside json files, soon will be update in dashboard
    # support action change only until layer3
    
    json_data = {
        "priority": 40000,
        "isPermanent": True,
        "deviceId": None,
        "treatment": {
            "instructions": [
                {
                    "type": "OUTPUT",
                    "port": None
                },
                {
                    "type": "L2MODIFICATION",
                    "subtype": "VLAN_ID",
                    "vlanId": None
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

    #Device ID
    # jika key deviceid tidak ditemukan didalam dict data. hapus key didalam json_data files
    try:
        data['deviceid']
    except KeyError:
        del json_data["deviceId"]
    else:
        json_data['deviceId']=data['deviceid']

    #Selector In Port
    try:
        data['selector.criteria.type.in_port']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IN_PORT"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IN_PORT"), None)
        json_data['selector']['criteria'][list]['port']=data['selector.criteria.type.in_port.value']

    #Selector eth src
    try:
        data['selector.criteria.type.eth_src']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_SRC"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_SRC"), None)
        json_data['selector']['criteria'][list]['mac']=data['selector.criteria.type.eth_src.value']

    #Selector eth dst
    try:
        data['selector.criteria.type.eth_dst']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_DST"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_DST"), None)
        json_data['selector']['criteria'][list]['mac']=data['selector.criteria.type.eth_dst.value']

    #Selector Eth Type
    try:
        data['selector.criteria.type.eth_type']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_TYPE"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_TYPE"), None)
        json_data['selector']['criteria'][list]['ethType']=data['selector.criteria.type.eth_type.value']

    #Selector vlan id
    try:
        data['selector.criteria.type.vlan_vid']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "VLAN_VID"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "VLAN_VID"), None)
        json_data['selector']['criteria'][list]['vlanId']=data['selector.criteria.type.vlan_vid.value']

    #Selector ip proto
    try:
        data['selector.criteria.type.ip_proto']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IP_PROTO"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IP_PROTO"), None)
        json_data['selector']['criteria'][list]['protocol']=data['selector.criteria.type.ip_proto.value']

    #Selector ipv4 src
    try:
        data['selector.criteria.type.ipv4_src']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IPV4_SRC"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IPV4_SRC"), None)
        json_data['selector']['criteria'][list]['ip']=data['selector.criteria.type.ipv4_src.value']

    #Selector ipv4 dst
    try:
        data['selector.criteria.type.ipv4_dst']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IPV4_DST"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IPV4_DST"), None)
        json_data['selector']['criteria'][list]['ip']=data['selector.criteria.type.ipv4_dst.value']

    #Selector tcp src
    try:
        data['selector.criteria.type.tcp_src']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "TCP_SRC"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "TCP_SRC"), None)
        json_data['selector']['criteria'][list]['tcpPort']=data['selector.criteria.type.tcp_src.value']

    #Selector tcp dst
    try:
        data['selector.criteria.type.tcp_dst']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "TCP_DST"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "TCP_DST"), None)
        json_data['selector']['criteria'][list]['tcpPort']=data['selector.criteria.type.tcp_dst.value']

    #Selector udp src
    try:
        data['selector.criteria.type.udp_src']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "UDP_SRC"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "UDP_SRC"), None)
        json_data['selector']['criteria'][list]['udpPort']=data['selector.criteria.type.udp_src.value']

    #Selector udp dst
    try:
        data['selector.criteria.type.udp_dst']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "UDP_DST"), None)
        del json_data['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "UDP_DST"), None)
        json_data['selector']['criteria'][list]['udpPort']=data['selector.criteria.type.udp_dst.value']

    #instruction output
    try:
        data['treatment.instructions.output']
    except KeyError:
        list = next((index for (index, d) in enumerate(json_data['treatment']['instructions']) if d["type"] == "OUTPUT"), None)
        del json_data['treatment']['instructions'][list]
    else:
        list = next((index for (index, d) in enumerate(json_data['treatment']['instructions']) if d["type"] == "OUTPUT"), None)
        json_data['treatment']['instructions'][list]['port']=data['treatment.instructions.output.value']

    #instruction vlan id
    try:
        data['treatment.instructions.vlanid']
    except KeyError:
        list = search(json_data['treatment']['instructions'],key='subtype', value='VLAN_ID')
        del json_data['treatment']['instructions'][list]
    else:
        list = search(json_data['treatment']['instructions'],key='subtype', value='VLAN_ID')
        json_data['treatment']['instructions'][list]['vlanId']=data['treatment.instructions.vlanid.value']

    #instruction eth src
    try:
        data['treatment.instructions.eth_src']
    except KeyError:
        list = search(json_data['treatment']['instructions'],key='subtype', value='ETH_SRC')
        del json_data['treatment']['instructions'][list]
    else:
        list = search(json_data['treatment']['instructions'],key='subtype', value='ETH_SRC')
        json_data['treatment']['instructions'][list]['mac']=data['treatment.instructions.eth_src.value']

    #instruction eth dst
    try:
        data['treatment.instructions.eth_dst']
    except KeyError:
        list = search(json_data['treatment']['instructions'],key='subtype', value='ETH_DST')
        del json_data['treatment']['instructions'][list]
    else:
        list = search(json_data['treatment']['instructions'],key='subtype', value='ETH_DST')
        json_data['treatment']['instructions'][list]['mac']=data['treatment.instructions.eth_dst.value']

    #instruction ipv4 src
    try:
        data['treatment.instructions.ipv4_src']
    except KeyError:
        list = search(json_data['treatment']['instructions'],key='subtype', value='IPV4_SRC')
        del json_data['treatment']['instructions'][list]
    else:
        list = search(json_data['treatment']['instructions'],key='subtype', value='IPV4_SRC')
        json_data['treatment']['instructions'][list]['ip']=data['treatment.instructions.ipv4_src.value']

    #instruction ipv4 dst
    try:
        data['treatment.instructions.ipv4_dst']
    except KeyError:
        list = search(json_data['treatment']['instructions'],key='subtype', value='IPV4_DST')
        del json_data['treatment']['instructions'][list]
    else:
        list = search(json_data['treatment']['instructions'],key='subtype', value='IPV4_DST')
        json_data['treatment']['instructions'][list]['ip']=data['treatment.instructions.ipv4_dst.value']

    api_json = json.dumps(json_data)
    url = 'http://127.0.0.1:8181/onos/v1/flows'+data['deviceid']
    requests.post(url=url,  auth=("onos", "rocks"), data=api_json, headers={"content-type":"application/json"})
    return ("success!")


@app.route('/provisioning')
def provisioning():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('provisioning.html')


@app.route('/provisioning/openvswitch')
def openvswitch():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('openvswitch.html')


@app.route('/provisioning/mikrotik')
def mikrotik():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('mikrotik.html')


@app.route('/provisioning/api', methods=['POST'])
def openvswitch_api():
    raw = request.form.to_dict(flat=True)
    data = {k.encode('utf8'): v.encode('utf8') for k, v in raw.items()}

    if data["device-type"] == "openvswitch":
        os.system("export ANSIBLE_HOST_KEY_CHECKING=False")
        os.system('ansible-playbook -u %s -i %s, /opt/PureFlow/ansible/playbook/openvswitch.yaml --extra-vars "controller=%s bridge=%s"' %
                  (data["username"], data["device-ip"], data["controller"], data["bridge"]))
        return "success!"

    if data["device-type"] == "mikrotik":
        os.system("export ANSIBLE_HOST_KEY_CHECKING=False")
        os.system("ansible all -i %s, -m raw -a '/openflow add name=%s controllers=%s; /openflow enable %s;  quit' -u %s --extra-vars 'ansible_password=%s ansible_port=%s'" %
                  (data["device-ip"], data["bridge"], data["controller"], data["bridge"], data["username"], data["password"], data["port"]))
        return "success!"

    if data["device-type"] == "mikrotik-port":
        os.system("export ANSIBLE_HOST_KEY_CHECKING=False")
        os.system("ansible all -i %s, -m raw -a '/openflow port add switch=%s interface=%s disable=no;  quit' -u %s --extra-vars 'ansible_password=%s ansible_port=%s'" %
                  (data["device-ip"], data["bridge"], data["interface"], data["username"], data["password"], data["port"]))
        return "success!"


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host="0.0.0.0", port=4000, debug=True)
