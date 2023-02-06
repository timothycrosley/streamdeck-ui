This is technically unsupported until wayland provides a way to make global shortcuts, but...

# Key bindings passthrough
Some wayland compositors such as `Hyprland` provide a way to pass through some key bindings to specific applications, event when they're not in focus:

```
bind=ALT,R,pass,obs
bind=ALT,1,pass,obs
bind=ALT,2,pass,obs
bind=ALT,3,pass,obs

```
Doing so AFTER you assigned the aforementioned key bindings in OBS (or other software) will allow for OBS to receive those keybindings even when not in focus.

# Streamdeck-ui: send keys
The issue: `streamdeck-ui` already receives keystrokes from the Streamdeck, but can't emulate the corresponding keystrokes to complete the action under wayland.

The solution: install [dotool](https://git.sr.ht/%7Egeb/dotool) (you read it right, without the leading x) which behave like `xdotool` but works on a lower level, simulating mouse and keyboard events. Then you can simply specify specify `streamdeck-ui` a command to execute like `/path/to/the/script.sh` instead of a keypress.

`script.sh` should look like this:

```
#!/bin/bash
echo "key alt+2" | dotool
```

That's it!

Each keystroke will take about half a second or more to actuate. This can be improved, read dotool documentation to know how.

