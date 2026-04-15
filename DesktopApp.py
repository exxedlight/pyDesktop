import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk
from pathlib import Path
import sys

from DesktopGrid import *

class DesktopApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.exx.quickdesktop")
    
    def do_activate(self):
        win = DesktopGrid(self)

        # === Css loading ===
        script_dir = Path(sys.argv[0]).parent.resolve()
        css_path = script_dir / "style.css"
        if css_path.exists():
            css_provider = Gtk.CssProvider()
            css_provider.load_from_path(str(css_path))
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        else:
            print(f"CSS not found: {css_path}")
        # === /CSS ===

        win.present()