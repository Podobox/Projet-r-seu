import pygame

pygame.init()

# Définir la taille des fenêtres
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Créer la première fenêtre
screen1 = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Première fenêtre')

# Créer un bouton dans la première fenêtre pour afficher la deuxième fenêtre
button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 - 25, 100, 50)

# Créer la deuxième fenêtre
screen2 = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Deuxième fenêtre')

# Créer un bouton dans la deuxième fenêtre pour la fermer
exit_button = pygame.image.load('./Images/exit_game.png')
exit_button_rect = exit_button.get_rect()
exit_button_rect.topright = (WINDOW_WIDTH - 10, 10)

# Variables pour déterminer quelle fenêtre est actuellement affichée
current_screen = screen1
other_screen = screen2

# Boucle principale
while True:

    # Vérifier les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Vérifier si l'utilisateur clique sur le bouton dans la première fenêtre pour afficher la deuxième fenêtre
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                current_screen = screen2
                other_screen = screen1

        # Vérifier si l'utilisateur clique sur le bouton dans la deuxième fenêtre pour la fermer
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if exit_button_rect.collidepoint(event.pos):
                pygame.quit()
                quit()

    # Effacer l'écran
    current_screen.fill((255, 255, 255))

    # Dessiner le bouton pour afficher la deuxième fenêtre dans la première fenêtre
    pygame.draw.rect(current_screen, (0, 0, 255), button_rect)
    font = pygame.font.SysFont(None, 24)
    text = font.render('Afficher la deuxième fenêtre', True, (255, 255, 255))
    current_screen.blit(text, (button_rect.x + 10, button_rect.y + 10))

    # Dessiner le bouton pour fermer la deuxième fenêtre
    if current_screen == screen2:
        current_screen.blit(exit_button, exit_button_rect)

    # Mettre à jour l'écran
    pygame.display.update()

    # Si la deuxième fenêtre est affichée, afficher également la première fenêtre
    if current_screen == screen2:
        other_screen.blit(pygame.transform.scale(screen1, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.update()
