from gi.repository import Gtk, Gdk
import gi
import os
gi.require_version('Gtk', '4.0')


class AppIcon(Gtk.Box):
    def __init__(self, icon_name, label, cmd, config_item, save_callback):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        self.cmd = cmd
        self.config_item = config_item
        self.save_callback = save_callback

        px, py = map(int, config_item["pos"].split())
        self.init_x, self.init_y = px, py   # initial location
        self._last_mx, self._last_my = 0, 0 # last move location (cursor on drag)
        
        self.drag_align = True          # use grid align?
        self.grid_x_step = 40           # grid step X
        self.grid_y_step = 40           # grid stem Y

        self._pressed = False           # is LMB pressen on icon?
        self._is_drag = False           # is dragging performing?
        
        self.add_css_class("app-icon")

        # Icon item construction
        lbl_icon = Gtk.Label(label=icon_name, css_classes=["icon"])
        lbl_text = Gtk.Label(label=label, css_classes=["text"])
        lbl_text.set_xalign(0.5)
        lbl_text.set_justify(Gtk.Justification.CENTER)
        lbl_text.set_halign(Gtk.Align.CENTER)
        self.append(lbl_icon)
        self.append(lbl_text)

        # Events
        # --- click
        click = Gtk.GestureClick()
        click.set_button(Gdk.BUTTON_PRIMARY)
        click.connect("pressed", self._on_press)
        click.connect("released", self._on_release)
        self.add_controller(click)
        # --- drag (motion)
        motion = Gtk.EventControllerMotion()
        motion.connect("motion", self._on_motion)
        self.add_controller(motion)

        # Clickable
        self.set_cursor_from_name("pointer")

    

    def _launch_app(self):
        import subprocess
        import shlex
        
        # Run new process on empty workspace
        subprocess.run(["hyprctl", "dispatch", "togglespecialworkspace", "magic"])  # close special:magic
        subprocess.run(["hyprctl", "dispatch", "workspace", "empty"])               # switch to first empty workspace
        cmd = self.cmd.strip()
        parts = shlex.split(cmd)
        if not parts: return
        if parts[0] == "kitty":
            subprocess.Popen(["kitty", "fish", "-c", " ".join(parts[1:])])          # if kitty script
        else:
            expanded = [os.path.expanduser(arg) for arg in parts]                   # else - just launch
            subprocess.Popen(expanded)
    


    # --- DRAG LOGIC

    def _on_press(self, gesture, n_press, x, y):
        self._pressed = True
        self._is_drag = False
        px, py = self.get_parent().get_child_position(self)
        self._drag_start_x, self._drag_start_y = px, py
        self._last_mx, self._last_my = x, y


    def _on_motion(self, controller, x, y):
        if not self._pressed:
            return
        if not self._is_drag:
            if abs(x - self._last_mx) > 4 or abs(y - self._last_my) > 4:
                self._is_drag = True
        if self._is_drag:
            # DEBUG
            # print(f"Drag start: ({self._drag_start_x} {self._drag_start_y})")
            # print(f"Motion xy: ({x} {y})")
            # print(f"Parent: {self.get_parent().get_child_position(self)}")

            new_x = self._drag_start_x + x
            new_y = self._drag_start_y + y

            self.get_parent().move(self, new_x, new_y)
            self._drag_start_x = new_x
            self._drag_start_y = new_y


    def _on_release(self, gesture, n_press, x, y):
        if self._is_drag:
            fx, fy = self.get_parent().get_child_position(self)
            # DEBUG
            # print(f"fx, fy (before): {fx} {fy}")

            # Adjust to grid size
            if self.drag_align:
                fx = fx - (fx % self.grid_x_step)
                fy = fy - (fy % self.grid_y_step)

            if fy < 50: fy = 50
            if fx < 50: fx = 50

            # DEBUG
            # print(f"fx fy (after): {fx} {fy}")

            self.get_parent().move(self, fx, fy)
            self.config_item["pos"] = f"{int(fx)} {int(fy)}"
            self.save_callback()
        else:
            self._launch_app()
        
        self._pressed = False
        self._is_drag = False