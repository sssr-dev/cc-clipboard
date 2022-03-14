import os
import sys


def stop():
    cmd = 'ps ax | grep "ython script.py"'
    print("$", cmd)
    o = os.popen(cmd).read()
    print(o)
    cmd = f"kill {o.split(' ')[0]}"
    print("$", cmd)
    print(os.popen(cmd).read())


def start():
    stop()
    cmd = 'nohup python3 script.py > cc.log &'
    print("$", cmd)
    print(os.popen(cmd).read())


def main():
    print()
    args = sys.argv[1]
    if args == "start":

        start()
    elif args == "stop":
        stop()


if __name__ == '__main__':
    main()
