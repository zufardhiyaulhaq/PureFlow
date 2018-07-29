from flask import Flask, render_template, session, redirect, flash
from flask import request

import os
import ast
import json

app = Flask(__name__)

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
        return render_template('configuring.html')

@app.route('/configuring/api', methods = ['POST'])
def configuring_api():
    raw = request.form.to_dict(flat=True)
    data = {k.encode('utf8'): v.encode('utf8') for k, v in raw.items()}

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

@app.route('/provisioning/api', methods = ['POST'])
def openvswitch_api():
    raw = request.form.to_dict(flat=True)
    data = {k.encode('utf8'): v.encode('utf8') for k, v in raw.items()}

    if data["device-type"] == "openvswitch":
        os.system("export ANSIBLE_HOST_KEY_CHECKING=False")
        os.system('ansible-playbook -u %s -i %s, /opt/PureFlow/ansible/playbook/openvswitch.yaml --extra-vars "controller=%s bridge=%s"'%(data["username"],data["device-ip"],data["controller"],data["bridge"]))
        return "success!"
    
    if data["device-type"] == "mikrotik":
        os.system("export ANSIBLE_HOST_KEY_CHECKING=False")
        os.system("ansible all -i %s, -m raw -a '/openflow add name=%s controllers=%s; /openflow enable %s;  quit' -u %s --extra-vars 'ansible_password=%s ansible_port=%s'"%(data["device-ip"],data["bridge"],data["controller"],data["bridge"],data["username"],data["password"],data["port"]))
        return "success!" 
    
    if data["device-type"] == "mikrotik-port":
        os.system("export ANSIBLE_HOST_KEY_CHECKING=False")
        os.system("ansible all -i %s, -m raw -a '/openflow add port switch=%s interface=%s;  quit' -u %s --extra-vars 'ansible_password=%s ansible_port=%s'"%(data["device-ip"],data["bridge"],data["interface"],data["username"],data["password"],data["port"]))
        return "success!"

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host="0.0.0.0", port=4000, debug=True)

