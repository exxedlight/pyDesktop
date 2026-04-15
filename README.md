# PyDesktop

~ Simple desktop solution for Hyprland, writen on python (GTK-4).
![Screenshot](/screenshots/1.png)

## Installation

Just download *.zip, and unpack anywhere you want. Give execution rights:
```bash
chmod +x path/to/the/main.py
```

Then, just execute:
```bash
path/to/the/main.py
```

In my configuration, I use it with this in my *~/.config/hypr/hyprland.conf*: 
1. *exec-once = ~/OWN/PyDesktop/main.py*
2. *bind = $mainMod, D, togglespecialworkspace, magic*
3. Windowrule to launch it on special:magic workspace:
```conf
windowrule { 
    name = quickdesktop
    match:class = com.exx.quickdesktop
    workspace = special:magic
}
```

With this, I have autorunned desktop-module on *special:magic* workspace on system startup, and can toggle it with *Super+D* bind.

## Config

Create *desktop.json* file in the root of project (where *main.py* exist). See structure on desktop_example.json.
1. pos: coordinates, where icon located
2. icon: use Nerd font for icons, just paste it here
3. command: command, which will be executed on click
4. label: text under the icon

## Notes

- It`s no ability to add/remove icons from app in this version. Only derectly desktop.json manipulations.
- Icons drag feature implemented, so you can just create icon in desktop.json with "pos": "0 0" and move it in any place with mouse inside app.