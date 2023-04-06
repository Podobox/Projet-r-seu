from Controller.Menu import run
import pygame as pg
import subprocess
import os
from Controller.Backup import Backup
from Controller.Controller import Controller
if __name__ == '__main__':
    pg.display.set_caption("Caesar3")
    # Check if c_daemon is already running
    process = subprocess.Popen(['pgrep', 'c_daemon'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    if output:
        # c_daemon is already running
        print("c_daemon is already running")
    else:
        # c_daemon is not running, start it
        print("Starting c_daemon")
        subprocess.Popen([os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'c_daemon', 'bin', 'c_daemon'))])

    run()
    #Controller(Backup().load("new"))
    exit(0)

