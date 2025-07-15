import pygame
from pygame.locals import *
from input import handle_input

# Initialize Pygame
pygame.init()

# Set up window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Fill the screen with a color (e.g., black)
    screen.fill((0, 0, 0))



    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()