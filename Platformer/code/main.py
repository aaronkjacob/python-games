import pygame
import os
import math
import random
from os import listdir
from os.path import isfile, join


# Initialize Pygame
pygame.init()

# Set up window dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

BG_COLOR = ('white')  # White background
FPS = 60  # Frames per second

PLAYER_VELOCITY = 5  # Player movement speed



def main(screen):
    clock = pygame.time.Clock() # Initialize the clock
    running = True # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Fill the screen with the background color
        screen.fill(BG_COLOR)


        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main(screen)

