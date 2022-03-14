import os
import pyperclip
from pynput import keyboard
import time
import requests as rq

copy_hotkey = "<ctrl>+c" if os.uname().sysname.lower() != "darwin" else "<cmd>+c"


def get_link_or_no():
    time.sleep(0.3)
    pcp: str = pyperclip.paste()
    lpcps = len(pcp.split("."))
    if lpcps > 1:
        if any((pcp.startswith("http://"), pcp.startswith("https://"))):
            if not pcp.startswith("https://cc.sssr.dev"):
                r = rq.get("https://api.sssr.dev/cc?create="+pcp).json()['object']['short']
                print(f"{pcp} => {r}")
                pyperclip.copy(r)


listener = keyboard.GlobalHotKeys({copy_hotkey: get_link_or_no})

if __name__ == '__main__':
    listener.start()
    listener.join()