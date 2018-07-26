from flask import Flask, render_template
from flask import request

import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/provisioning')
def provisioning():
    return render_template('provisioning.html')

@app.route('/provisioning/openvswitch')
def openvswitch():
    return render_template('openvswitch.html')

@app.route('/provisioning/api', methods = ['POST'])
def openvswitch_api():
    # data = request.get_json() ##tidak support atau belum support form di dashboard
    
    data = request.form.to_dict(flat=True)
    print (data)
    print (type(data))
    print (data["device-type"])
    print (type(data["device-type"]))
    # if data["device-type"] == "openvswitch":
    #     os.system('ansible-playbook -u %s -i %s, /opt/PureFlow/ansible/playbook/openvswitch/openvswitch.yaml --extra-vars "controller=%s bridge=%s"'%(data["username"],data["device-ip"],data["controller"],data["bridge"]))
    #     return "success!"
    return "success!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)

