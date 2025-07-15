import pygame
import sys
from ExtractSpriteSheet import SpriteSheet  # Import the SpriteSheet class from the other file

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Sheet Tutorial")


class Player:
  def __init__(self,x,y):
    self.x = x
    self.y = y
  def load_sprite_sheet(self):
    sprite_sheet_image = pygame.image.load("assets/MainCharacters/NinjaFrog/idle.png").convert_alpha() # Load the sprite sheet image

    # create animation list
    self.animation_list = []
    self.animation_steps = 10
    self.last_update = pygame.time.get_ticks()
    self.animation_cooldown = 40 # milliseconds
    self.frame = 0

    for x in range(self.animation_steps):
      self.animation_list.append(SpriteSheet.get_image(sprite_sheet_image, 32, 32, x, 2))  # Get each frame of the sprite sheet
  def draw_sprite_sheet(self):
    current_time = pygame.time.get_ticks()
    if current_time - self.last_update >= self.animation_cooldown:
      self.last_update = current_time
      self.frame += 1
      if self.frame >= len(self.animation_list):
        self.frame = 0
    screen.blit(self.animation_list[self.frame], (self.x,self.y))  # Draw the current frame of the sprite sheet at the center of the screen

player = Player(0,0)
player.load_sprite_sheet()

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

    player.draw_sprite_sheet()  # Draw the sprite sheet animation

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
