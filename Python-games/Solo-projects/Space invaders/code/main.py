import pygame
import sys
import random


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
    self.speed = 10
    self.rect = pygame.Rect(self.x,self.y,50,50)
    self.surf = pygame.surface.Surface((50,50),pygame.SRCALPHA)
    self.surf.fill('blue')
    self.damage = 10
  def draw(self):
    screen.blit(self.surf, self.rect)
  def update(self):
    self.rect.x += self.vx
    self.draw()

bullet_delay_count = 0
bullet_delay = 20

class PlayerBullet(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.x = player.rect.centerx
    self.y = player.rect.top
    self.vy = 0
    self.speed = 40
  def draw(self):
    pygame.draw.circle(screen, 'white', (self.x,self.y), 10)
    self.vy = self.speed
    self.y -= self.vy
    if self.y < 0:
      self.kill()
      playerBullets.remove(self)

class enemy(pygame.sprite.Sprite):
  def __init__(self, x, y, width, height):
    super().__init__()
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.color = 'white'
    self.START_HEALTH = 16
    self.health = self.START_HEALTH
    self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
    self.surf = pygame.Surface((self.rect.width,self.rect.height))
    self.health_width = self.width    

  def draw(self):
    self.surf.fill(self.color)
    screen.blit(self.surf,self.rect)
    self.color = 'white'
    self.health_rect = pygame.draw.rect(screen, 'red', (self.x, self.rect.top - 20,self.health_width,10))
    self.health_width = self.width*(self.health/self.START_HEALTH)

class Text():
  def __init__(self,text,fontSize,coordinates, color):
    self.text = text
    self.fontSize = fontSize
    self.coordinates = coordinates
    self.font = pygame.font.Font(None, fontSize)
    self.color = color
  def draw(self):
    text = self.font.render(self.text, True, str(self.color))
    text_rect = text.get_rect(center=(self.coordinates))
    screen.blit(text, text_rect)

def UpdateWaves(wave):
  if wave <= 3 and len(invaders) <= 0:
    if wave == 1:
      for i in range(5):
        invaders.append(enemy(250*i + 100,100,40,40))
    if wave == 2:
      for i in range(6):
        invaders.append(enemy(210*i + 100,100,40,40))
    if wave == 3:
      for i in range(7):
        invaders.append(enemy(random.randint(180,200)*i + 100,100,40,40))
  elif wave > 3 and len(invaders) <= 0:
    for i in range(7):
      invaders.append(enemy(random.randint(180,200)*i + 100,100,40,40))
      invader.health += 10


player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT-100)
playerBullets = []

invaders = []
wave = 1


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

    Text(('wave: ' + str(wave)),50,(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 'red').draw()

    for invader in invaders:
      invader.draw()

    player.update()

    if bullet_delay_count > bullet_delay:
      playerBullets.append(PlayerBullet())
      bullet_delay_count = 0

    UpdateWaves(wave)

    for bullet in playerBullets:
      bullet.draw()
      for invader in invaders:
        if invader.rect.collidepoint(bullet.x,bullet.y) or invader.rect.collidepoint(bullet.x - 8,bullet.y) or invader.rect.collidepoint(bullet.x+8,bullet.y):
          invader.health -= player.damage
          invader.color = 'red'
          bullet.kill()
          playerBullets.remove(bullet)
        if invader.health <= 0:
          invader.kill()
          invaders.remove(invader)
          

    if len(invaders) <= 0:
      wave += 1
    print(len(invaders))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
