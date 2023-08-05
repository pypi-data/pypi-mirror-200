import os
import subprocess

def man_page():
    MAN_DIR = "/docs/e2e_cli.1"
    # print("curent folder(cli)", os.path.dirname(__file__))
    MAN_PATH=os.path.dirname(__file__)+MAN_DIR
    # print(MAN_PATH)
    subprocess.call(["man", MAN_PATH])

    