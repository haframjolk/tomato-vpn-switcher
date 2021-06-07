#!/usr/bin/env python3

from flask import Flask, render_template
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
    """Starts the VPN"""
    send_ssh_command(["service", config["ovpn_service"], "start"])


def stop_vpn():
    """Stops the VPN"""
    send_ssh_command(["service", config["ovpn_service"], "stop"])


def select_server(address: str):
    # TODO
    pass


@app.route("/")
def index():
    return render_template("index.html", hosts=config["ovpn_hosts"])
