# Tomato VPN Switcher

A Flask-based web app to switch OpenVPN servers on a Tomato-based router. Designed and tested with NordVPN in mind.

## Prerequisites

Epsilon requires Python 3.9 or later and [Poetry](https://python-poetry.org).

## Setup

```sh
git clone https://github.com/haframjolk/tomato-vpn-switcher.git
cd tomato-vpn-switcher
poetry install
```

## Configuration

This program is configured using a JSON file placed in the repository root called `config.json`. Copy the included `config.example.json` and change the values to match your setup. Make sure to do all the required VPN setup on your router, through the web interface, as this program only switches the server address. This program does not currently support password authentication for SSH, use public key authentication instead.

## Running

### Development

```sh
poetry shell
FLASK_ENV=development flask run
```

### Production

```sh
poetry shell
./serve.py
```
