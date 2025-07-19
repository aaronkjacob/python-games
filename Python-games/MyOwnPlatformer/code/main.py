import pygame
import sys
from input import handle_inputs

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.gravity_speed = 8
        self.jump_height = 12
        self.jump_count = 0
        self.image = pygame.Surface((40, 40))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def movement(self, inputs):
      if handle_inputs()['a']:
        self.vx = -self.speed
      elif handle_inputs()['d']:
        self.vx = self.speed
      else:
        self.vx = 0
      self.rect.x += self.vx
      self.rect.y += self.vy
    def draw(self):
        screen.blit(self.image, self.rect)
    def jump(self):
        self.rect.y += self.gravity_speed
        self.gravity_speed += .8
        if player.rect.bottom >= SCREEN_HEIGHT:
          self.rect.y -= 1
          self.vy = 0
          self.gravity_speed = 0
          self.jump_count = 0
          
        if handle_inputs()['space'] and self.jump_count < 2:
          self.gravity_speed = -self.jump_height
          self.jump_count += 1

    def tileCollisoin(self):
      # Top player top tile collision
      collided_blocks = []
      for block in all_tiles:
        if self.rect.colliderect(block.rect):
          collided_blocks.append(block)
          for collided in collided_blocks:
            if self.rect.bottom > collided.rect.top:
              self.rect.y -= 1
              self.vy = 0
              self.gravity_speed = 0
              self.jump_count = 0
            elif self.rect.left < collided.rect.right and self.rect.bottom-5<collided.rect.bottom:
              self.rect.x += 10
              self.rect.y += 5
              print('hi')
            elif self.rect.right > collided.rect.left and self.rect.top-5>collided.rect.top:
              self.rect.x -= 5
              self.rect.y += 5
              print('collisoin')

class tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size, offset):
        super().__init__()
        self.surf = pygame.surface.Surface((size,size))
        self.surf.fill('blue')
        self.rect = pygame.Rect(x-offset,y,size,size)
    def draw(self):
      pygame.draw.rect(screen, 'darkgreen', self.rect)
      pygame.draw.rect(screen, 'black', self.rect, 1)
    

player = Player(400,0)

offset_x = 0

running = True
while running:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False

  screen.fill('black')

  floor = []
  extra_tiles = []
  extra_tiles.append(tile(75,SCREEN_HEIGHT-75*2,75,offset_x))
  all_tiles = [*floor, *extra_tiles]

  if player.rect.x > SCREEN_WIDTH-200:
    offset_x += 5
    player.rect.x -= 5
  if player.rect.x < 200:
    offset_x -= 5
    player.rect.x += 5


  for i in range(15):
      all_tiles.append(tile(i*75,SCREEN_HEIGHT-75,75, offset_x))
      for block in all_tiles:
        block.draw()

  player.draw()
  player.movement(handle_inputs())
  player.jump()
  player.tileCollisoin()

  
  

  pygame.display.flip()
  clock.tick(60)

pygame.quit()
sys.exit()