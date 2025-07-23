import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Road Rush")

# road image
road_image = pygame.image.load('Python-games/Road-rush/assets/road.png').convert_alpha()
road_image = pygame.transform.scale(road_image, (SCREEN_WIDTH,SCREEN_HEIGHT))


class Player(pygame.sprite.Sprite): 
  def __init__(self, x, y):
    super().__init__()
    self.x = x
    self.y = y
    self.speed = 7
    self.image = pygame.image.load('Python-games/Road-rush/assets/motor-bike.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (100,100))
    self.rect = pygame.Rect(self.x, self.y, 80,100)
    self.rect = pygame.Rect((self.rect.x + 10, self.rect.y, self.rect.width, self.rect.height))
  def move(self):
    dx = 0
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        dx = -self.speed
    if key[pygame.K_d]:
        dx = self.speed

    # check for collision with the wall
    if player.rect.right + dx >= SCREEN_WIDTH - 35:
      dx = 0
    if player.rect.left + dx <= 20:
      dx = 0

    
    self.rect.x += dx

  def draw(self):
    screen.blit(self.image, self.rect)
    pygame.draw.rect(screen, 'white', self.rect, 2)

class Obstacle(pygame.sprite.Sprite):
  def __init__(self, *groups):
    super().__init__(*groups)
    self.pick_image = 1
    if self.pick_image == 1:
      self.image = pygame.image.load('Python-games/Road-rush/assets/blue-car.png').convert_alpha()
      self.image = pygame.transform.scale(self.image, (200,200))
    self.rect = self.image.get_rect()
    self.rect.x = SCREEN_HEIGHT/2
  def draw(self):
    screen.blit(self.image, self.rect)
    pygame.draw.rect(screen, 'white', self.rect,2)

obstacle_group = pygame.sprite.Group()
obstacle_group.add(Obstacle())

road_scroll = 0

def draw_bg(road_scroll):
  screen.blit(road_image, (0,road_scroll))
  screen.blit(road_image, (0,road_scroll-SCREEN_HEIGHT))

# Set up clock
clock = pygame.time.Clock()
FPS = 60

# create player instance
player = Player(SCREEN_WIDTH/2 - 43, SCREEN_HEIGHT-150)

# Main game loop
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

  # Fill the screen with a color (e.g., black)
  screen.fill((0, 0, 0))

  draw_bg(road_scroll)
  road_scroll += 10
  if road_scroll >= SCREEN_HEIGHT:
    road_scroll = 0

  player.move()
  player.draw()

  for obstacle in obstacle_group:
    obstacle.draw()


  # Update the display
  pygame.display.flip()
  clock.tick(FPS)

pygame.quit()
sys.exit()
