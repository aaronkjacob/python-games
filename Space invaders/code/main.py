import pygame
import sys
from input import keyPressed

pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
  def __init__(self,x,y):
    super().__init__()
    self.x = x
    self.y = y
    self.vx = 0
    self.speed = 8
    self.rect = pygame.Rect(self.x,self.y,50,50)
    self.surf = pygame.surface.Surface((50,50),pygame.SRCALPHA)
    self.surf.fill('red')
  def draw(self):
    screen.blit(self.surf, self.rect)
  def move(self):
    if keyPressed() == 'd':
      self.vx = self.speed
    elif keyPressed() == 'a':
      self.vx = -self.speed
    else:
      self.vx = 0
  def bullet(self):
    pass
  def update(self):
    self.rect.x += self.vx
    self.draw()
    self.move()
      

player = Player(SCREEN_WIDTH/2, 600)
playerBullets = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    player.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
