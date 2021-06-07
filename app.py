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


def start_vpn():
    """Starts the VPN, returns the exit code"""
    return send_ssh_command(f"service vpnclient{config['ovpn_client_no']} start")


def stop_vpn():
    """Stops the VPN, returns the exit code"""
    return send_ssh_command(f"service vpnclient{config['ovpn_client_no']} stop")


def select_server(address: str):
    """Selects the specified address as the VPN server, returns the exit code"""
    return send_ssh_command(f"nvram set vpn_client{config['ovpn_client_no']}_addr={address}")


def set_status(address: str, enabled: bool):
    """Sets the VPN server address and enabled state, returns the exit code"""
    return send_ssh_command(f"""nvram set vpn_client{config['ovpn_client_no']}_addr={address} &&
                                service vpnclient{config['ovpn_client_no']} {'start' if enabled else 'stop'}""")


@app.route("/")
def index():
    return render_template("index.html", hosts=config["ovpn_hosts"])


@app.route("/submit", methods=["POST"])
def submit():
    # Get form data
    data = request.form
    host = data.get("host")
    enabled = data.get("enabled") == "On"

    # If an invalid host is submitted
    if all(h["address"] != host for h in config["ovpn_hosts"]):
        print(f"Error: {host} is not defined in the configuration file")
        # TODO: return error
        return "Error"

    # Set VPN status
    if set_status(host, enabled) != 0:
        print("Error: Could not update VPN settings")
        # TODO: return error
        return "Error"

    return "Success"
