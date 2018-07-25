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

@app.route('/provisioning/api')
def openvswitch_api():
    data = request.form.to_dict(flat=True)
    
    if data["device-type"] == "openvswitch":
        os.system('ansible-playbook /opt/PureFlow/ansible/playbook/openvswitch/openvswitch.yaml --ask-pass --extra-vars "host=%s user=%s controller=%s bridge=%s"'%(data["device-ip"],data["username"],data["controller"],data["bridge"]))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)

