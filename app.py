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


def send_ssh_command(command: list[str]):
    """Runs the specified command on the configured SSH server, returns the exit code"""
    code = subprocess.call(["ssh", "-l", config["ssh_user"], config["ssh_host"], *command])
    return code


def start_vpn():
    """Starts the VPN, returns the exit code"""
    return send_ssh_command(["service", config["ovpn_service"], "start"])


def stop_vpn():
    """Stops the VPN, returns the exit code"""
    return send_ssh_command(["service", config["ovpn_service"], "stop"])


def select_server(address: str):
    """Selects the specified address as the VPN server, returns the exit code"""
    return send_ssh_command(["set", f"vpn_client1_addr={address}"])


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
    if host not in config["ovpn_hosts"]:
        print(f"Error: {host} is not defined in the configuration file")
        # TODO: return error
        return

    # Select server
    if not select_server(host):
        print(f"Error: Could not set server to {host}")
        # TODO: return error
        return

    # Start or stop VPN depdending on choice
    if enabled:
        if not start_vpn():
            print("Error: Could not start VPN")
            # TODO: return error
            return
    else:
        if not stop_vpn():
            print("Error: Could not stop VPN")
            # TODO: return error
            return

    return "success"
