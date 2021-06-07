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

Elections are configured using a JSON file placed in the repository root called `config.json`. Copy the included `config.example.json` and change the values to match your setup.

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
