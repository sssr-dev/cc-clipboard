#!python3
import os
import sys
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
debug = False
endpoint = 'https://api.sssr.dev/cc'
if "-d" in sys.argv:
    debug = True
    endpoint = 'http://127.0.0.1:11491/cc'


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
            # noinspection PyUnresolvedReferences
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
                    r = rq.post(endpoint, data={"url": pcp}, params={"v": "1.1"})
                    if debug:
                        print(f'{r.text=} {r.url=} {r.headers=}', end='')
                    short_url = r.json()['object']['short']
                    if debug:
                        print(f'{short_url=}')
                    print(f"{pcp} => {short_url}")
                    pyperclip.copy(short_url)
                except Exception as e:
                    traceback.print_exc()
                    notification(f"Exception: {e!s}")


listener = keyboard.GlobalHotKeys({copy_hotkey: get_link_or_no})

if __name__ == '__main__':
    listener.start()
    listener.join()
