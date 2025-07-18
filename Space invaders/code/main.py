import pygame
import sys

pygame.init()
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 900
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

bullet_delay_count = 0
bullet_delay = 30

class PlayerBullet(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.x = player.rect.centerx
    self.y = player.rect.top
    self.vy = 0
    self.speed = 20
  def draw(self):
    pygame.draw.circle(screen, 'white', (self.x,self.y), 5)
    self.vy = self.speed
    self.y -= self.vy
    if self.y < 0:
      self.kill()
      playerBullets.remove(self)

player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT-100)
playerBullets = []

running = True
while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
      player.vx = -player.speed
    if keys[pygame.K_d]:
      player.vx = player.speed
    if (not keys[pygame.K_a]) and (not keys[pygame.K_d]):
      player.vx = 0

    bullet_delay_count+=1

    screen.fill((0, 0, 0))

    collision_rect = pygame.draw.rect(screen, 'white', (SCREEN_WIDTH/2,100,50,50))

    player.update()

    if bullet_delay_count > bullet_delay:
      playerBullets.append(PlayerBullet())
      bullet_delay_count = 0


    for bullet in playerBullets:
      bullet.draw()
      if collision_rect.collidepoint(bullet.x, bullet.y):
        pygame.draw.rect(screen, 'red', (SCREEN_WIDTH/2,100,50,50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
