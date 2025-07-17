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
    self.vx = 0
    self.speed = 8
    self.rect = pygame.Rect(self.x,self.y,50,50)
    self.surf = pygame.surface.Surface((50,50),pygame.SRCALPHA)
    self.surf.fill('red')
  def draw(self):
    screen.blit(self.surf, self.rect)
  def update(self):
    self.rect.x += self.vx
    self.draw()

class PlayerBullet(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.x = player.rect.centerx
    self.y = player.rect.top
    self.vy = 0
    self.speed = 20
    self.delay = 0
  def draw(self):
    self.delay += 1
    pygame.draw.circle(screen, 'white', (self.x,self.y), 5)
    self.vy = self.speed
    self.y -= self.vy
    if self.y < 0:
      self.kill()
    

player = Player(SCREEN_WIDTH/2, 600)
playerBullets = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
      playerBullets.append(PlayerBullet())
    if keys[pygame.K_a]:
      player.vx = -player.speed
    if keys[pygame.K_d]:
      player.vx = player.speed
    
    if (not keys[pygame.K_a]) and (not keys[pygame.K_d]):
      player.vx = 0

    screen.fill((0, 0, 0))

    player.update()


    for bullet in playerBullets:
      bullet.draw()
      bullet.delay = 0


    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
