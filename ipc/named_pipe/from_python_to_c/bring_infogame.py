import pygame as pg
import tkinter as tk
import os

root = tk.Tk()
WINDOW_WIDTH = root.winfo_screenwidth()
WINDOW_HEIGHT = root.winfo_screenheight()

def main():
    pg.init()
    path = "MYFIFO3"
    os.mkfifo(path)
    quit = False
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pg.time.Clock()

    while not quit:
        fifo = open(path,"w")
        for event in pg.event.get():
            if event.type == pg.QUIT:
                fifo.write('end')
                fifo.close()
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    fifo.write('end')
                    fifo.close()
                    pg.quit()    
            if event.type == pg.MOUSEBUTTONDOWN:
                background = pygame.image.load('Images/_fired_00001.png')
                background = pygame.transform.scale(background, x)
                menu_page = True

        pg.display.flip()

if __name__ == '__main__':
    main()