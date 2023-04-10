from Controller.Menu import run
import pygame as pg
from Controller.Backup import Backup
from Controller.Controller import Controller
if __name__ == '__main__':
    pg.display.set_caption("Caesar3")
    run()
    #Controller(Backup().load("new"))
    exit(0)