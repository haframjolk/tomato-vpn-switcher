#!/usr/bin/env python3

from flask import Flask, render_template, request
import json
import subprocess


def init():
    """Initialize program data"""
    global config

    # Read config
    with open("config.json") as f:
        config = json.load(f)


# Initialize data
init()
# Initialize app
app = Flask(__name__)


def send_ssh_command(command: str):
    """Runs the specified command on the configured SSH server, returns the exit code"""
    code = subprocess.call(["ssh", "-l", config["ssh_user"], config["ssh_host"], command])
    return code


def set_status(address: str, enabled: bool):
    """Sets the VPN server address and enabled state, returns the exit code"""
    # The client is restarted if desired on, to make sure the server address is changed
    # Otherwise, it is stopped
    return send_ssh_command(f"""nvram set vpn_client{config['ovpn_client_no']}_addr={address}
                                service vpnclient{config['ovpn_client_no']} {'restart' if enabled else 'stop'}""")


def get_ssh_output(command: str):
    """Runs the specified command via SSH and returns its output as a string"""
    out = subprocess.check_output(["ssh", "-l", config["ssh_user"], config["ssh_host"], command])
    return out.decode().strip()


def get_status():
    """Returns the currently selected VPN server's address and whether or not the client is running"""
    # If /etc/openvpn/vpnclient{n} exists, the client is running
    address, status = get_ssh_output(f"""nvram get vpn_client{config['ovpn_client_no']}_addr;
                                         if [ -f /etc/openvpn/vpnclient{config['ovpn_client_no']} ]
                                         then
                                             echo 'on'
                                         else
                                             echo 'off'
                                         fi""").split("\n")
    # Return the data as a dict
    out = {
        "server": address,
        "enabled": status == "on",
    }
    return out


@app.route("/")
def index():
    status = get_status()
    return render_template("index.html", hosts=config["ovpn_hosts"], status=status)


@app.route("/submit", methods=["POST"])
def submit():
    # Get form data
    data = request.form
    host = data.get("host")
    enabled = data.get("enabled") == "on"

    # If an invalid host is submitted
    if all(h["address"] != host for h in config["ovpn_hosts"]):
        print(f"Error: {host} is not defined in the configuration file")
        return render_template("error.html", message=f"{host} is not defined in the configuration file.")

    # Set VPN status
    if set_status(host, enabled) != 0:
        print("Error: Settings change failed")
        return render_template("error.html")

    return render_template("success.html")
