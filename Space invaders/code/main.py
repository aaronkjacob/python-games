import pygame
import sys

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
    self.rect = pygame.Rect(self.x,self.y,50,50)
    self.surf = pygame.surface.Surface((50,50),pygame.SRCALPHA)
    self.surf.fill('red')
  def draw(self):
    screen.blit(self.surf, self.rect)

player = Player(SCREEN_WIDTH/2, 600)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    player.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
