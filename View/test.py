import pygame

pygame.init()
main_surface = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Créez une surface de fenêtre contextuelle
popup_surface = pygame.Surface((300, 200))
popup_surface.fill((255, 255, 255))

# Créez un rectangle pour la position de la fenêtre contextuelle
popup_rect = popup_surface.get_rect(center=main_surface.get_rect().center)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Si le bouton gauche de la souris est cliqué, afficher la fenêtre contextuelle
            main_surface.blit(popup_surface, popup_rect)
    
    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
