#!python3
import os
import time
import platform
import traceback

from pynput import keyboard
import requests as rq
import pyperclip

try:
    import win10toast
except ImportError:
    win10toast = None


copy_hotkey = "<ctrl>+c" if os.uname().sysname.lower() != "darwin" else "<cmd>+c"
plt = platform.system()


def notification(message):
    title = "SSSR cc clipboard"
    if plt == "Darwin":
        command = f'''
        osascript -e 'display notification "{message}" with title "{title}"'
        '''
    elif plt == "Linux":
        command = f'''
        notify-send "{title}" "{message}"
        '''
    elif plt == "Windows":
        if win10toast is not None:
            win10toast.ToastNotifier().show_toast(title, message)
        return
    else:
        return
    os.system(command)


def get_link_or_no():
    time.sleep(0.3)
    pcp: str = pyperclip.paste()
    lpcps = len(pcp.split("."))
    if lpcps > 1:
        if pcp.startswith("http://") or pcp.startswith("https://"):
            if not pcp.startswith("https://cc.sssr.dev"):
                try:
                    r = rq.post("https://api.sssr.dev/cc", data={"url": pcp}, params={"v": "1.1"}).json()
                    short_url = r['object']['short']
                    print(f"{pcp} => {short_url}")
                    pyperclip.copy(short_url)
                except Exception as e:
                    traceback.print_exc()
                    notification(f"Exception: {e!s}")


listener = keyboard.GlobalHotKeys({copy_hotkey: get_link_or_no})

if __name__ == '__main__':
    listener.start()
    listener.join()
