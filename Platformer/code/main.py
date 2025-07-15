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

def get_background(name):
    # Load background image
    image = pygame.image.load(join("assets", "backgrounds", name))
    __, __, width, height = image.get_rect()
    tiles = []

    for i in range(SCREEN_WIDTH // width + 1):
        for j in range(SCREEN_HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image

def draw(screen,background, bg_image):
    for tile in background:
        screen.blit(bg_image, tile)
    pygame.display.update()

def main(screen):
    clock = pygame.time.Clock() # Initialize the clock

    background, bg_image = get_background("Blue.png")  # Load the background image

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
        draw(screen,background,bg_image)

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main(screen)

