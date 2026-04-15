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
    opacity = 1.0 override
    no_blur = off
    border_size = 0
    decorate = off
    workspace = special:magic
}
```

## Config