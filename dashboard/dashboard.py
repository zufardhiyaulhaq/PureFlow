from flask import Flask, render_template, session, redirect, flash
from flask import request

import os
import ast
import json
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)


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
    # Priority, Permanent, is not defined in form
    
    json = {
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
                },
                {
                    "type": "L4MODIFICATION",
                    "subtype": "TCP_SRC",
                    "tcpPort": None
                },
                {
                    "type": "L4MODIFICATION",
                    "subtype": "UDP_SRC",
                    "udpPort": None
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
    # jika key deviceid tidak ditemukan didalam dict data. hapus key didalam json files
    try:
        data['deviceid']
    except KeyError:
        del json["deviceId"]
    else:
        json['deviceId']=data['deviceid']

    #Selector In Port
    try:
        data['selector.criteria.type.in_port']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "IN_PORT"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "IN_PORT"), None)
        json['selector']['criteria'][list]['port']=data['selector.criteria.type.in_port.value']

    #Selector eth src
    try:
        data['selector.criteria.type.eth_src']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "ETH_SRC"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "ETH_SRC"), None)
        json['selector']['criteria'][list]['mac']=data['selector.criteria.type.eth_src.value']

    #Selector eth dst
    try:
        data['selector.criteria.type.eth_dst']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "ETH_DST"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "ETH_DST"), None)
        json['selector']['criteria'][list]['mac']=data['selector.criteria.type.eth_dst.value']

    #Selector Eth Type
    try:
        data['selector.criteria.type.eth_type']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "ETH_TYPE"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "ETH_TYPE"), None)
        json['selector']['criteria'][list]['ethType']=data['selector.criteria.type.eth_type.value']

    #Selector vlan id
    try:
        data['selector.criteria.type.vlan_vid']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "VLAN_VID"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "VLAN_VID"), None)
        json['selector']['criteria'][list]['vlanId']=data['selector.criteria.type.vlan_vid.value']

    #Selector ip proto
    try:
        data['selector.criteria.type.ip_proto']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "IP_PROTO"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "IP_PROTO"), None)
        json['selector']['criteria'][list]['protocol']=data['selector.criteria.type.ip_proto.value']

    #Selector ipv4 src
    try:
        data['selector.criteria.type.ipv4_src']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "IPV4_SRC"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "IPV4_SRC"), None)
        json['selector']['criteria'][list]['ip']=data['selector.criteria.type.ipv4_src.value']

    #Selector ipv4 dst
    try:
        data['selector.criteria.type.ipv4_dst']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "IPV4_DST"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "IPV4_DST"), None)
        json['selector']['criteria'][list]['ip']=data['selector.criteria.type.ipv4_dst.value']

    #Selector tcp src
    try:
        data['selector.criteria.type.tcp_src']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "TCP_SRC"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "TCP_SRC"), None)
        json['selector']['criteria'][list]['tcpPort']=data['selector.criteria.type.tcp_src.value']

    #Selector tcp dst
    try:
        data['selector.criteria.type.tcp_dst']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "TCP_DST"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "TCP_DST"), None)
        json['selector']['criteria'][list]['tcpPort']=data['selector.criteria.type.tcp_dst.value']

    #Selector udp src
    try:
        data['selector.criteria.type.udp_src']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "UDP_SRC"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "UDP_SRC"), None)
        json['selector']['criteria'][list]['udpPort']=data['selector.criteria.type.udp_src.value']

    #Selector udp dst
    try:
        data['selector.criteria.type.udp_dst']
    except KeyError:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "UDP_DST"), None)
        del json['selector']['criteria'][list]
    else:
        list = next((index for (index, d) in enumerate(json['selector']['criteria']) if d["type"] == "UDP_DST"), None)
        json['selector']['criteria'][list]['udpPort']=data['selector.criteria.type.udp_dst.value']

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
