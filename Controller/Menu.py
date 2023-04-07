import pygame
from pygame.locals import *
from Controller.Controller import Controller
from Controller.Backup import Backup
from Controller.Communication import Communication
from Model.Game import Game
from View.Visualizer import WINDOW_WIDTH, WINDOW_HEIGHT
import Save

pygame.init()
pygame.font.init()

# La fenêtre du jeu
pygame.display.set_caption("Caesar3")  # on met le titre du jeu
res = (2000, 1100)
screen = pygame.display.set_mode(res, FULLSCREEN)
x = screen.get_size()  # tuple de taille de l'écran
# le logo du jeu:
logo = pygame.image.load('Images/logo.png')
logo = pygame.transform.scale(logo, (270, 200))
# Images pour le menu:
start_game = pygame.image.load('Images/start_game.png').convert_alpha()
start_game = pygame.transform.scale(start_game, (275, 30))
start_game_button = pygame.image.load('Images/start_game_button.png').convert_alpha()
start_game_button = pygame.transform.scale(start_game_button, (275, 30))
start_game_rect = start_game.get_rect()
start_game_rect.x = (x[0] / 2) - 100
start_game_rect.y = (x[1] / 3)
load_game = pygame.image.load('Images/load_game.png').convert_alpha()
load_game = pygame.transform.scale(load_game, (275, 30))
load_game_button = pygame.image.load('Images/load_game_button.png').convert_alpha()
load_game_button = pygame.transform.scale(load_game_button, (275, 30))
load_game_rect = load_game.get_rect()
load_game_rect.x = (x[0] / 2) - 100
load_game_rect.y = (x[1] / 3) + 50
exit = pygame.image.load('Images/exit.png').convert_alpha()
exit = pygame.transform.scale(exit, (275, 30))
exit_button = pygame.image.load('Images/exit_button.png').convert_alpha()
exit_button = pygame.transform.scale(exit_button, (275, 30))
exit_rect = exit.get_rect()
exit_rect.x = (x[0] / 2) - 100
exit_rect.y = (x[1] / 3) + 120
globe = pygame.image.load('Images/globe.png').convert_alpha()
globe = pygame.transform.scale(globe, (70, 70))
globe_button = pygame.image.load('Images/globe_button.png').convert_alpha()
globe_button = pygame.transform.scale(globe_button, (70, 70))
globe_rect = globe.get_rect()
globe_rect.x = (x[0]) - 150
globe_rect.y = (x[1]) - 150
# menu parties enregistres
saved_games = pygame.image.load('Images/captur_savedgames.png').convert_alpha()
saved_games = pygame.transform.scale(saved_games, (400, 150))
zone_de_texte = pygame.image.load('Images/zone_de_texte.png')
zone_de_texte = pygame.transform.scale(zone_de_texte, (300, 50))
running = True
menu_page = False
saved_games_menu = False
a = False
param = False
start_new_game = False


def button(panel, mouse):
    # soit 275 la largeur et 30 la hauteur de chaque panel
    if panel.x + panel.width > mouse[0] > panel.x and panel.y + panel.height > mouse[1] > panel.y:
        return True
    else:
        return False


sound_play = True


def menu():
    x = screen.get_size()
    global menu_page
    global running
    global saved_games_menu
    global sound_play

    global start_new_game

    # sound()
    # pygame.mixer.music.load('Sound/Rome4.mp3')
    # pygame.mixer.music.play()
    while menu_page:

        screen.blit(logo, ((x[0] / 2) - 100, (x[1] / 15)))
        screen.blit(start_game, ((x[0] / 2) - 100, (x[1] / 3)))
        screen.blit(load_game, ((x[0] / 2) - 100, (x[1] / 3) + 60))
        screen.blit(globe, ((x[0]) - 150, (x[1]) - 150))
        screen.blit(exit, ((x[0] / 2) - 100, (x[1] / 3) + 120))
        # pygame.display.flip()
        mouse = pygame.mouse.get_pos()
        if button(exit_rect, mouse):
            screen.blit(exit_button, ((x[0] / 2) - 100, (x[1] / 3) + 120))
        if button(start_game_rect, mouse):
            screen.blit(start_game_button, ((x[0] / 2) - 100, (x[1] / 3)))
        if button(load_game_rect, mouse):
            screen.blit(load_game_button, ((x[0] / 2) - 100, (x[1] / 3) + 60))
        if button(globe_rect, mouse):
            screen.blit(globe_button, ((x[0]) - 150, (x[1]) - 150))
        pygame.display.flip()
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button(exit_rect, mouse):
                    running = False
                    pygame.quit()
                    quit()
                if button(start_game_rect, mouse):
                    # pygame.mixer.music.stop()
                    # pygame.mixer.music.load('Sound/Rome1.mp3')
                    # pygame.mixer.music.play()
                    start_new_game = 1
                    start()
                    # Controller()

                if (button(load_game_rect, mouse)):
                    menu_page = 0
                    saved_games_menu = 1
                    saved()
                if(button(globe_rect, mouse)):
                    menu_page = 0
                    saved_games_menu = 1
                    connect()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE) or (event.key == pygame.K_SPACE):
                    running = False
                    pygame.quit()


def start():
    global start_new_game
    global param
    while start_game:
        nom = ""
        back_1 = pygame.image.load('Images/start_game_background.png')
        back_1 = pygame.transform.scale(back_1, x)
        screen.blit(back_1, (0, 0))
        screen.blit(saved_games, ((x[0] / 2) - 200, x[1] / 3))
        screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 3) + 50))
        font = pygame.font.Font(None, 24)
        text = font.render("Enter city name: ", True, (0, 0, 0))
        screen.blit(text, ((x[0] / 2) - 150, (x[1] / 3) + 20))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                    else:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                pygame.quit()
                                quit(0)
                            else:
                                param = 1
                                enter_start_game()


def enter_start_game():
    global param
    x = screen.get_size()
    font = pygame.font.Font(None, 24)
    nom = ""
    # pygame.display.flip()
    while param:

        for event in pygame.event.get():
            if event.type == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                quit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    nom = nom[:-1]
                    screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 3) + 50))
                    text_2 = font.render(nom, True, (0, 0, 0))
                    screen.blit(text_2, (x[0] / 2 - 100, (x[1] / 3) + 70))
                    pygame.display.flip()
                elif event.key == pygame.K_RETURN:
                    game = Game(1000)
                    (Backup(nom)).save(game)
                    Controller(nom, game=game)
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit(0)
                    carac = event.dict['unicode']
                    nom = nom + carac
                    screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 3) + 50))
                    text_2 = font.render(nom, True, (0, 0, 0))
                    screen.blit(text_2, (x[0] / 2 - 100, (x[1] / 3) + 70))
                    pygame.display.flip()


def saved():
    global saved_games_menu
    global menu_page
    global running
    global a
    while saved_games_menu:
        back_1 = pygame.image.load('Images/_fired_00001.png')
        back_1 = pygame.transform.scale(back_1, x)
        screen.blit(back_1, (0, 0))

        #saved_games = pygame.transform.scale(saved_games, (275,300))
        screen.blit(saved_games, ((x[0] / 2) - 200, x[1] / 3))
        screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 3) + 50))
        font = pygame.font.Font(None, 24)
        text = font.render("Enter city name: ", True, (0, 0, 0))
        screen.blit(text, ((x[0] / 2) - 150, (x[1] / 3) + 20))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                    else:
                        a = True
                        enter_saved_game()
                        # for i in Save:


def connect():
    global saved_games_menu
    global menu_page
    global running
    global a
    while saved_games_menu:
        back_1 = pygame.image.load('Images/_fired_00001.png')
        back_1 = pygame.transform.scale(back_1, x)
        screen.blit(back_1, (0, 0))

        #saved_games = pygame.transform.scale(saved_games, (275,300))
        screen.blit(saved_games, ((x[0] / 2) - 200, x[1] / 3))
        screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 3) + 50))
        font = pygame.font.Font(None, 24)
        text = font.render("Enter city name: ", True, (0, 0, 0))
        screen.blit(text, ((x[0] / 2) - 150, (x[1] / 3) + 20))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                    else:
                        a = True
                        enter_connect_game()
                        # for i in Save:


def enter_connect_game():
    global a
    global sound_play
    x = screen.get_size()
    font = pygame.font.Font(None, 24)
    ip_port = ""
    erreur = ""
    # pygame.display.flip()
    while(a):

        for event in pygame.event.get():
            if (event.type == pygame.K_ESCAPE):
                running = False
                pygame.quit()
                quit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    ip_port = ip_port[:-1]
                    screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 3) + 50))
                    text_2 = font.render(ip_port, True, (0, 0, 0))
                    screen.blit(text_2, (x[0] / 2 - 100, (x[1] / 3) + 70))
                    pygame.display.flip()
                elif event.key == pygame.K_RETURN:
                    communication = Communication()
                    if ip_port.count("/") != 1:
                        erreur = "no port provided"
                        text_erreur = font.render(erreur, True, (255, 0, 0))
                        screen.blit(text_erreur, ((x[0] / 2) - 50, (x[1] / 3) + 100))
                        pygame.display.flip()
                        continue
                    ip, port = ip_port.split("/")
                    nom, players = communication.connect(ip, int(port))
                    backup = Backup(nom)
                    game = backup.load(nom)
                    if game is None:
                        erreur = "host does not exist"
                        text_erreur = font.render(erreur, True, (255, 0, 0))
                        screen.blit(text_erreur, ((x[0] / 2) - 50, (x[1] / 3) + 100))
                        pygame.display.flip()
                    else:
                        Controller(nom, game=game)
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit(0)
                    carac = event.dict['unicode']
                    ip_port = ip_port + carac
                    text_2 = font.render(ip_port, True, (0, 0, 0))
                    screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 3) + 50))
                    screen.blit(text_2, (x[0] / 2 - 100, (x[1] / 3) + 70))
                    pygame.display.flip()


def enter_saved_game():
    global a
    global sound_play
    x = screen.get_size()
    font = pygame.font.Font(None, 24)
    nom = ""
    erreur = ""
    # pygame.display.flip()
    while(a):

        for event in pygame.event.get():
            if (event.type == pygame.K_ESCAPE):
                running = False
                pygame.quit()
                quit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    nom = nom[:-1]
                    screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 3) + 50))
                    #supp_text= pygame.image.load("Images/supp_text.png")
                    text_2 = font.render(nom, True, (0, 0, 0))
                    screen.blit(text_2, (x[0] / 2 - 100, (x[1] / 3) + 70))
                    pygame.display.flip()
                elif event.key == pygame.K_RETURN:
                    backup = Backup(nom)
                    game = backup.load(nom)
                    if game is None:
                        erreur = "file does not exist"
                        text_erreur = font.render(erreur, True, (255, 0, 0))
                        screen.blit(text_erreur, ((x[0] / 2) - 50, (x[1] / 3) + 100))
                        pygame.display.flip()
                    else:
                        Controller(nom, game=game)
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit(0)
                    carac = event.dict['unicode']
                    nom = nom + carac
                    text_2 = font.render(nom, True, (0, 0, 0))
                    screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 3) + 50))
                    screen.blit(text_2, (x[0] / 2 - 100, (x[1] / 3) + 70))
                    pygame.display.flip()


def run():
    global running
    global menu_page
    # Ecran d'accueil:
    background = pygame.image.load('Images/caesar3.png')  # genere une surface
    background = pygame.transform.scale(background, x)  # redimonssione
    while running:
        screen.blit(background, (0, 0))
        first_click = 0
        if menu_page:
            menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE) or (event.key == pygame.K_SPACE):
                    running = False
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Apparition du menu
                background = pygame.image.load('Images/_fired_00001.png')
                background = pygame.transform.scale(background, x)
                menu_page = True
        pygame.display.flip()
