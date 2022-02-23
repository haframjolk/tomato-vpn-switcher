#!/usr/bin/env python3

import webview
from app import app

webview.create_window("Tomato VPN Switcher", app, height=1100)
webview.start()
