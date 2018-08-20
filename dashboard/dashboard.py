from flask import Flask, render_template, session, redirect, flash, request

import os
import ast
import json
import MySQLdb
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

db_config_raw = json.loads(open("config.json","r").read())
db_config = {k.encode('utf8'): v.encode('utf8') for k, v in db_config_raw.items()}

# get user table
def db_user():
    db = MySQLdb.connect(host=db_config["ip"],user=db_config["username"],passwd=db_config["password"],db=db_config["database"])
    cursor = db.cursor() 
    
    sql = "select * from user"
    cursor.execute(sql)
    results = cursor.fetchall()

    return results

# get controller table
def db_controller():
    db = MySQLdb.connect(host=db_config["ip"],user=db_config["username"],passwd=db_config["password"],db=db_config["database"])    
    cursor = db.cursor() 
    
    sql = "select * from controller"
    cursor.execute(sql)
    results = cursor.fetchall()

    return results

# get site_settings table
def db_site():
    db = MySQLdb.connect(host=db_config["ip"],user=db_config["username"],passwd=db_config["password"],db=db_config["database"])    
    cursor = db.cursor() 
    
    sql = "select * from site_settings"
    cursor.execute(sql)
    results = cursor.fetchall()

    return results

# check table user, if wrong, return False
def login_check(user,password):
    results = db_user()

    for row in results:
        if user == row[1]:
            if password == row[2]:
                return True
            else:
                return False
        else:
            return False

# fungsi untuk mencari nomor list yang berada di dictionary
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

# get data from onos
def get(append):
    url = 'http://127.0.0.1:8181/onos/v1'+append
    data = requests.get(url, auth=HTTPBasicAuth(
        'onos', 'rocks')).text.decode('utf-8')
    return json.loads(data)

# main menu
@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')

# logout menu
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect("/")

# login menu
@app.route('/login', methods=['POST'])
def admin_login():
    # masukan data kedalam fungsi db_user_check
    if login_check(request.form['username'],request.form['password']):
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return redirect("/")

# menu configuring, menampilkan semua devices dengan fungsi get
@app.route('/configuring')
def configuring():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        data = get("/devices")
        return render_template('configuring.html', data=data)

# menu spesific configuring devices
@app.route('/configuring/api', methods=['POST', 'GET'])
def device():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        raw = request.form.to_dict(flat=True)
        data = {k.encode('utf8'): v.encode('utf8') for k, v in raw.items()}
        return render_template('configuring-device.html', data=data)

# kirimkan data to controller
@app.route('/configuring/controller', methods=['POST'])
def configuring_api():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        raw = request.form.to_dict(flat=True)
        res = {k.encode('utf8'): v.encode('utf8') for k, v in raw.items()}

        # variabel data diambil dari API
        data = dict((k, v) for k, v in res.iteritems() if v)

        # Priority, Permanent, is not defined in form, so we defined inside json files, soon will be update in dashboard
        # support action change only until layer3
        
        # variable json_data tetap, nanti akan diappend dari variable data
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

        # Device ID
        # jika key deviceid tidak ditemukan didalam dict data. hapus key didalam json_data files
        try:
            data['deviceid']
        except KeyError:
            del json_data["deviceId"]
        else:
            json_data['deviceId']=data['deviceid']

        # Selector In Port
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.in_port']
        except KeyError:
            # cari nomor list data in_port
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IN_PORT"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IN_PORT"), None)
            json_data['selector']['criteria'][list]['port']=data['selector.criteria.type.in_port.value']

        # Selector eth src
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.eth_src']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_SRC"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_SRC"), None)
            json_data['selector']['criteria'][list]['mac']=data['selector.criteria.type.eth_src.value']

        # Selector eth dst
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.eth_dst']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_DST"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_DST"), None)
            json_data['selector']['criteria'][list]['mac']=data['selector.criteria.type.eth_dst.value']

        # Selector Eth Type
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.eth_type']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_TYPE"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "ETH_TYPE"), None)
            json_data['selector']['criteria'][list]['ethType']=data['selector.criteria.type.eth_type.value']

        # Selector vlan id
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.vlan_vid']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "VLAN_VID"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "VLAN_VID"), None)
            json_data['selector']['criteria'][list]['vlanId']=data['selector.criteria.type.vlan_vid.value']

        # Selector ip proto
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.ip_proto']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IP_PROTO"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IP_PROTO"), None)
            json_data['selector']['criteria'][list]['protocol']=data['selector.criteria.type.ip_proto.value']

        # Selector ipv4 src
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.ipv4_src']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IPV4_SRC"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IPV4_SRC"), None)
            json_data['selector']['criteria'][list]['ip']=data['selector.criteria.type.ipv4_src.value']

        # Selector ipv4 dst
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.ipv4_dst']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IPV4_DST"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "IPV4_DST"), None)
            json_data['selector']['criteria'][list]['ip']=data['selector.criteria.type.ipv4_dst.value']

        # Selector tcp src
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.tcp_src']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "TCP_SRC"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "TCP_SRC"), None)
            json_data['selector']['criteria'][list]['tcpPort']=data['selector.criteria.type.tcp_src.value']

        # Selector tcp dst
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.tcp_dst']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "TCP_DST"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "TCP_DST"), None)
            json_data['selector']['criteria'][list]['tcpPort']=data['selector.criteria.type.tcp_dst.value']

        # Selector udp src
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.udp_src']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "UDP_SRC"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "UDP_SRC"), None)
            json_data['selector']['criteria'][list]['udpPort']=data['selector.criteria.type.udp_src.value']

        # Selector udp dst
        # jika tidak ada data, delete, jika ada append
        try:
            data['selector.criteria.type.udp_dst']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "UDP_DST"), None)
            del json_data['selector']['criteria'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['selector']['criteria']) if d["type"] == "UDP_DST"), None)
            json_data['selector']['criteria'][list]['udpPort']=data['selector.criteria.type.udp_dst.value']

        # instruction output
        # jika tidak ada data, delete, jika ada append
        try:
            data['treatment.instructions.output']
        except KeyError:
            list = next((index for (index, d) in enumerate(json_data['treatment']['instructions']) if d["type"] == "OUTPUT"), None)
            del json_data['treatment']['instructions'][list]
        else:
            list = next((index for (index, d) in enumerate(json_data['treatment']['instructions']) if d["type"] == "OUTPUT"), None)
            json_data['treatment']['instructions'][list]['port']=data['treatment.instructions.output.value']

        # instruction vlan id
        # jika tidak ada data, delete, jika ada append
        try:
            data['treatment.instructions.vlanid']
        except KeyError:

            list = search(json_data['treatment']['instructions'],key='subtype', value='VLAN_ID')
            del json_data['treatment']['instructions'][list]
        else:
            list = search(json_data['treatment']['instructions'],key='subtype', value='VLAN_ID')
            json_data['treatment']['instructions'][list]['vlanId']=data['treatment.instructions.vlanid.value']

        # instruction eth src
        # jika tidak ada data, delete, jika ada append
        try:
            data['treatment.instructions.eth_src']
        except KeyError:
            list = search(json_data['treatment']['instructions'],key='subtype', value='ETH_SRC')
            del json_data['treatment']['instructions'][list]
        else:
            list = search(json_data['treatment']['instructions'],key='subtype', value='ETH_SRC')
            json_data['treatment']['instructions'][list]['mac']=data['treatment.instructions.eth_src.value']

        # instruction eth dst
        # jika tidak ada data, delete, jika ada append
        try:
            data['treatment.instructions.eth_dst']
        except KeyError:
            list = search(json_data['treatment']['instructions'],key='subtype', value='ETH_DST')
            del json_data['treatment']['instructions'][list]
        else:
            list = search(json_data['treatment']['instructions'],key='subtype', value='ETH_DST')
            json_data['treatment']['instructions'][list]['mac']=data['treatment.instructions.eth_dst.value']

        # instruction ipv4 src
        # jika tidak ada data, delete, jika ada append
        try:
            data['treatment.instructions.ipv4_src']
        except KeyError:
            list = search(json_data['treatment']['instructions'],key='subtype', value='IPV4_SRC')
            del json_data['treatment']['instructions'][list]
        else:
            list = search(json_data['treatment']['instructions'],key='subtype', value='IPV4_SRC')
            json_data['treatment']['instructions'][list]['ip']=data['treatment.instructions.ipv4_src.value']

        # instruction ipv4 dst
        # jika tidak ada data, delete, jika ada append
        try:
            data['treatment.instructions.ipv4_dst']
        except KeyError:
            list = search(json_data['treatment']['instructions'],key='subtype', value='IPV4_DST')
            del json_data['treatment']['instructions'][list]
        else:
            list = search(json_data['treatment']['instructions'],key='subtype', value='IPV4_DST')
            json_data['treatment']['instructions'][list]['ip']=data['treatment.instructions.ipv4_dst.value']

        # dump dictionary kedalam json
        api_json = json.dumps(json_data)

        # push json kedalam controller
        url = 'http://127.0.0.1:8181/onos/v1/flows/'+data['deviceid']
        requests.post(url=url,  auth=("onos", "rocks"), data=api_json, headers={"content-type":"application/json"})

        # return success
        return ("success!")

# Provisioning Menu
@app.route('/provisioning')
def provisioning():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('provisioning.html')

# Provisioning openvswitch
@app.route('/provisioning/openvswitch')
def openvswitch():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('openvswitch.html')

# provisioning mikrotik
@app.route('/provisioning/mikrotik')
def mikrotik():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('mikrotik.html')

# api provisioning
@app.route('/provisioning/api', methods=['POST'])
def provisioning_api():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        raw = request.form.to_dict(flat=True)
        data = {k.encode('utf8'): v.encode('utf8') for k, v in raw.items()}

        # jika device type openvswitch
        if data["device-type"] == "openvswitch":
            os.system("export ANSIBLE_HOST_KEY_CHECKING=False")
            os.system('ansible-playbook -u %s -i %s, /opt/PureFlow/ansible/playbook/openvswitch.yaml --extra-vars "controller=%s bridge=%s"' %
                    (data["username"], data["device-ip"], data["controller"], data["bridge"]))
            return "success!"

        # jika device type mikrotik
        if data["device-type"] == "mikrotik":
            os.system("export ANSIBLE_HOST_KEY_CHECKING=False")
            os.system("ansible all -i %s, -m raw -a '/openflow add name=%s controllers=%s; /openflow enable %s;  quit' -u %s --extra-vars 'ansible_password=%s ansible_port=%s'" %
                    (data["device-ip"], data["bridge"], data["controller"], data["bridge"], data["username"], data["password"], data["port"]))
            return "success!"

        # jika provisioning mikrotik port
        if data["device-type"] == "mikrotik-port":
            os.system("export ANSIBLE_HOST_KEY_CHECKING=False")
            os.system("ansible all -i %s, -m raw -a '/openflow port add switch=%s interface=%s disable=no;  quit' -u %s --extra-vars 'ansible_password=%s ansible_port=%s'" %
                    (data["device-ip"], data["bridge"], data["interface"], data["username"], data["password"], data["port"]))
            return "success!"

# Admin Menu
@app.route('/admin', methods=['GET'])
def admin():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        user = db_user()
        controller = db_controller()
        site = db_site()
        data = {
                    "user": {
                        "username": user[0][1],
                        "password": user[0][2],
                        "fullname": user[0][3]
                    },
                    "controller": {
                        "username": controller[0][1],
                        "password": controller[0][2],
                        "ip": controller[0][3]
                    },
                    "site": {
                        "port": site[0][1]
                    }
                }
        
        return render_template('admin.html', data=data)

# Admin API
@app.route('/admin/api', methods=['POST'])
def _api():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        raw = request.form.to_dict(flat=True)
        data = {k.encode('utf8'): v.encode('utf8') for k, v in raw.items()}

        if data["method"] == "profile":
                db = MySQLdb.connect(host=db_config["ip"],user=db_config["username"],passwd=db_config["password"],db=db_config["database"])
                cursor = db.cursor()
                cursor.execute("""
                UPDATE user
                SET username='%s', fullname='%s'
                WHERE id=1;
                """%(data["username"],data["fullname"]))
                db.commit()
                db.close()

                return "success!"

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    port = db_site()
    app.run(host="0.0.0.0", port=port[0][1], debug=True)
