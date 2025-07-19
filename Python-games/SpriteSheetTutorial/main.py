import pygame
import sys
from ExtractSpriteSheet import SpriteSheet  # Import the SpriteSheet class from the other file
from ExtractSpriteSheet import Animation  # Import the Animation class from the other file
from input import wasd_input  # Import the wasd_input function from the input module

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Sheet Tutorial")




class Player(Animation):
  def __init__(self, x, y, directory):
    super().__init__()  # Initialize the Animation class
    self.x = x
    self.y = y
    self.directory = directory
    self.load_sprite_sheet(directory, screen)  # Load the sprite sheet frames
  def draw(self):
    self.draw_sprite_sheet()  # Draw the sprite sheet animation


player = Player(400, 300, "assets/MainCharacters/NinjaFrog/idle.png")  # Create a player instance and load the sprite sheet
player.draw()


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

  if wasd_input()['d']:
    player.draw()  # Draw the idle sprite sheet
    player.x += 5  # Move right
  elif wasd_input()['a']:
    player.draw()  # Draw the idle sprite sheet
    player.x -= 5  # Move left
    
  player.draw()  # Draw the sprite sheet animation

  pygame.display.update()
  clock.tick(60)

pygame.quit()
sys.exit()
