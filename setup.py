import sys
from cx_Freeze import setup, Executable

APP_NAME = "Tomato VPN Switcher"

build_options = {
    "packages": [],
    "include_files": ["static", "templates", "config.json"],
    "excludes": []
}
bdist_msi_options = {
    "install_icon": "app-icon.ico"
}
bdist_mac_options = {
    "iconfile": "app-icon.icns",
    "bundle_name": APP_NAME,
    "custom_info_plist": "Info.plist"
}
bdist_dmg_options = {
    "volume_label": APP_NAME,
    "applications_shortcut": True
}

base = "Win32GUI" if sys.platform == "win32" else None

executables = [
    Executable("gui.py",
               base=base,
               targetName=APP_NAME,
               shortcutName=APP_NAME,
               shortcutDir="DesktopFolder",
               icon="app-icon.ico")
]

setup(name="Tomato VPN Switcher",
      version="1.0",
      description="A Flask-based web app to switch OpenVPN servers on a Tomato-based router",
      options={"build_exe": build_options,
               "bdist_msi": bdist_msi_options,
               "bdist_mac": bdist_mac_options,
               "bdist_dmg": bdist_dmg_options},
      executables=executables)
