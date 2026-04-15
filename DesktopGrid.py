import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import json
from pathlib import Path
import sys
from AppIcon import *

class DesktopGrid(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(application=app)
        self.set_decorated(False)

        self.script_dir = Path(sys.argv[0]).parent.resolve()
        self.config_path = self.script_dir / "desktop.json"

        fixed = Gtk.Fixed()
        fixed.add_css_class("desktop-bg")
        
        # Loading desktop.json
        try:
            with open(self.config_path, "r") as f:
                self.apps = json.load(f)
        except Exception as e:
            print(f"Desktop loading error ({self.config_path}): {e}")
            self.apps = []

        # Push items on grid
        for item in self.apps:
            x, y = map(int, item["pos"].split())
            icon_widget = AppIcon(item["icon"], item["label"], item["command"], item, self._save_config)
            icon_widget.set_size_request(64, 64)
            fixed.put(icon_widget, x, y)

        self.set_child(fixed)
        self.set_opacity(0.7)
    
    def _save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.apps, f, indent=2)