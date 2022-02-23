# Tomato VPN Switcher

![Tomato VPN Switcher logo](icon-256.png)

A Flask-based web app to switch OpenVPN servers on a Tomato-based router. Designed and tested with NordVPN in mind.

## Prerequisites

Tomato VPN Switcher requires Python 3.9 or later and [Poetry](https://python-poetry.org). It also requires SSH to be set up and in your PATH.

## Setup

```sh
git clone https://github.com/haframjolk/tomato-vpn-switcher.git
cd tomato-vpn-switcher
poetry install
```

## Configuration

This program is configured using a JSON file placed in the repository root called `config.json`. Copy the included `config.example.json` and change the values to match your setup. Make sure to do all the required VPN setup on your router, through the web interface, as this program only switches the server address. This program does not currently support password authentication for SSH, use public key authentication instead. Do note that by default, Tomato limits the number of allowed SSH connection attempts to 3 every 60 seconds, which can cause problems with this program. I recommend disabling the limit altogether.

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

### GUI mode

Tomato VPN Switcher has a GUI mode which uses pywebview to run the Flask app and display the interface in a web view, stopping the server when the web view is closed.

```sh
poetry shell
./gui.py
```

## Bundling

Tomato VPN Switcher can be bundled into an executable using cx_Freeze. The bundled executable will use the aforementioned GUI mode.

```sh
poetry shell
python setup.py [MODE]
```

Replace `[MODE]` with your preferred mode. Note that builds will only be created for the operating system and platform that they are created on.

### cx_Freeze modes

| Mode      | Platform              | Output          |
| --------- | --------------------- | --------------- |
| build     | Any                   | Folder          |
| bdist_mac | macOS                 | .app bundle     |
| bdist_dmg | macOS                 | .dmg disk image |
| bdist_msi | Windows               | MSI installer   |
| bdist_rpm | Linux (Red Hat-based) | RPM package     |

If the build is successful, you will find the output in either the `dist/` or `build/` directory, depending on the mode chosen.
