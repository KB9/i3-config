# -*- coding: utf-8 -*-
#
import subprocess
import os
import os.path

from i3pystatus import Status
from i3pystatus.updates import aptget
from i3pystatus import IntervalModule

class brightness(IntervalModule):
    interval = 1

    def get_brightness(self):
        command = "xrandr --verbose | grep \"Brightness\" | awk '{print $2;}'"
        result = subprocess.check_output(command, shell=True) # Byte string with \n
        result = result.decode("utf-8").strip() # To UTF-8 string
        value = float(result) * 100.0
        value = int(value)
        return value

    def run(self):
        self.output = {
            "full_text": "💡 %s%%" % str(self.get_brightness())
        }

status = Status()

# Displays clock like this:
# Tue 30 Jul 11:59:46 PM KW31
#                          ^-- calendar week

status.register("updates",
    format = "Updates: {count}",
    format_no_updates = "",
    on_leftclick="termite --geometry=1200x600 --title=updates -e 'pacaur --needed --noconfirm --noedit -Syu'",
    backends = [aptget.AptGet()])

status.register("clock",
    format="🕒 %H:%M:%S",
    color='#C678DD',
    interval=1,
    on_leftclick="/usr/bin/gsimplecal",)

status.register("clock",
    format="📅 %a %d %m %Y ",
    color='#61AEEE',
    interval=1,)


status.register("pulseaudio",
    color_unmuted='#98C379',
    color_muted='#E06C75',
    format_muted='🔉 [muted]',
    format="🔉 {volume}%")

status.register("network",
    interface="wlp7s0",
    color_up="#8AE234",
    color_down="#EF2929",
    format_up="📡 {essid} {kbs} kbs",
    format_down="",)


status.register("battery",
    battery_ident="BAT1",
    interval=5,
    format="🔋{status} {percentage:.0f}%",
    alert=True,
    alert_percentage=15,
    color="#FFFFFF",
    critical_color="#FF1919",
    charging_color="#E5E500",
    full_color="#D19A66",
    status={
        "DIS": "🔻",
        "CHR": "🔺",
        "FULL": "🔌",
},)

status.register("temp",
    color='#78EAF2',
    format="🌡️ {temp:.0f}°C",)

status.register("cpu_usage",
    on_leftclick="termite --title=htop -e 'htop'",
    format="⚡ {usage}%",)

status.register("mem",
    color="#999999",
    warn_color="#E5E500",
    alert_color="#FF1919",
    format="🐏 {avail_mem}/{total_mem} GB",
    divisor=1073741824,)

status.register("disk",
    color='#56B6C2',
    path="/home",
    on_leftclick="pcmanfm",
    format="🏠 {avail} GB",)

status.register("disk",
    hints = {"separator": False, "separator_block_width": 3},
    color='#ABB2BF',
    path="/",
    format="💽 {avail} GB",)

status.register(brightness)

status.run()