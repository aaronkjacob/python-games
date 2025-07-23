import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ninja Platformer")

# Set up clock
clock = pygame.time.Clock()
FPS = 60

# background image
bg_image = pygame.image.load('Python-games/Solo-projects/Ninja-platformer/assets/background.png')
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT+260))

# game variables
GRAVITY = 1

# player class
class Player(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    self.x = x
    self.y = y
    self.image = pygame.image.load('Python-games/Solo-projects/Ninja-platformer/assets/player/Ninja1.png')
    self.rect = pygame.Rect(x,y,self.image.get_width(),self.image.get_height())
    self.speed = 10
    self.flip = True
    self.gravity_speed = 5
    self.jump_count = 0
    self.vel_y = 0
  def move(self):
    dx = 0
    dy = 0

    # check for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
      dx = self.speed
      self.flip = False
    if keys[pygame.K_a]:
      dx = -self.speed
      self.flip = True

    self.vel_y += GRAVITY
    dy += self.vel_y


    if keys[pygame.K_SPACE] and self.jump_count < 1:
      self.vel_y = -20
      self.jump_count += 1

    # collision with bottom wall
    if self.rect.bottom + dy >= SCREEN_HEIGHT and dy > 0:
      dy = 0
      self.jump_count = 0

    self.rect.x += dx
    self.rect.y += dy

    print(dy)
  def draw(self):
    screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    pygame.draw.rect(screen, 'white', self.rect, 2)

# create an instance of player
player = Player(SCREEN_WIDTH/2, 0)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., black)
    screen.blit(bg_image, (0,0))

    # draw player on the screen
    player.move()
    player.draw()    

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
