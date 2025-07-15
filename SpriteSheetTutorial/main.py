import pygame
import sys
from ExtractSpriteSheet import SpriteSheet  # Import the SpriteSheet class from the other file

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Sheet Tutorial")



sprite_sheet_image = pygame.image.load("assets/MainCharacters/NinjaFrog/idle.png").convert_alpha() # Load the sprite sheet image



# create animation list
animation_list = []
animation_steps = 10
last_update = pygame.time.get_ticks()
animation_cooldown = 40 # milliseconds
frame = 0

for x in range(animation_steps):
  animation_list.append(SpriteSheet.get_image(sprite_sheet_image, 32, 32, x, 2))  # Get each frame of the sprite sheet

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
            pygame.quit()

    screen.fill('white')  # Fill the screen with black

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
      last_update = current_time
      frame += 1
      if frame >= len(animation_list):
          frame = 0
          


    screen.blit(animation_list[frame], (0, 0))


    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
