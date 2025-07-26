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
bg_image = pygame.image.load('assets/background/background.png').convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT+260)).convert_alpha()

# game variables
GRAVITY = 1
offset_x = 0
bg_offset = 0
scrolling = False
SCROLL_THRESH = 500
game_over = False

def tileMap(tileObj,tileList, enemyObj, enemyList):
# Create a floor of tiles across the bottom of the screen
  def tile_floor(tile_num,x,y):
    for i in range(tile_num):
      tile = tileObj(i*100 + x,y)
      tileList.append(tile)

  # starting tile floor
  tile_floor(12,0,700)

  # tile floor above ^ that one
  tile_floor(3, 500, 500)
  enemyList.append(enemyObj(600,SCREEN_HEIGHT-400))


  # tile floor after init tile floor
  tile_floor(4, 1400, 500)

  tile_floor(2, 2200, 400)

  tile_floor(1, 2600, 400)

  tile_floor(3, 3000, 400)
  enemyList.append(enemyObj(3200, 300))

  tile_floor(5, 3700, 300)
  enemyList.append(enemyObj(3900, 200))

  tile_floor(1, 4600, SCREEN_HEIGHT-100)

  tile_floor(6, 4900, SCREEN_HEIGHT-200)
  enemyList.append(enemyObj(5200, SCREEN_HEIGHT-300))

  tile_floor(1, 5200, SCREEN_HEIGHT-400)

  tile_floor(3, 5900, 500)

  tile_floor(2, 6600, 400)
  enemyList.append(enemyObj(6650, 300))

  tile_floor(1, 7300, 300)

  tile_floor(1, 7800, 400)

  #enemyList.clear()

# make font variable
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 30)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x,y))

# player class
class Player(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    self.x = x
    self.y = y
    self.animation_count = 1
    self.animage_frame = [0,1,2,3]
    self.image = pygame.image.load('assets/player/idle/Ninja1.png').convert_alpha()
    self.rect = pygame.Rect(x,y,80,90)
    self.speed = 10
    self.flip = False
    self.jump_count = 0
    self.vel_y = 0
    self.animation_speed = .1
    self.idle = True
    self.moving = False
  def move(self):
    global offset_x
    global bg_offset
    global scrolling
    global SCROLL_THRESH
    global game_over
    dx = 0
    dy = 0
 
    # check for key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
      dx = self.speed
      self.flip = False
      self.moving = True
      self.idle = False
    elif keys[pygame.K_a]:
      dx = -self.speed
      self.flip = True
      self.moving = True
      self.idle = False
    else:
      self.moving = False
      self.idle = True

    self.vel_y += GRAVITY
    dy += self.vel_y


    if keys[pygame.K_SPACE] and self.jump_count < 1:
      self.vel_y = -25
      self.jump_count += 1


    # collision with bottom wall
    if self.rect.bottom + dy >= SCREEN_HEIGHT and dy > 0:
      game_over = True
    # scrolling
    if self.rect.right > SCREEN_WIDTH-SCROLL_THRESH and dx > 0:
      dx = 0
      offset_x += self.speed
      bg_offset += self.speed
      scrolling = True
    elif self.rect.left < SCROLL_THRESH and dx < 0:
      dx = 0
      offset_x -= self.speed
      bg_offset -= self.speed
      scrolling = True
    else:
      scrolling = False


    # collision with tile
    for tile in tiles:
      if self.rect.colliderect(tile.rect):
        # collision with jumping on tile
        if dy > 0 and self.vel_y > 0:
          dy = .5
          self.vel_y = 0
          self.jump_count = 0
          self.rect.bottom = tile.rect.top
        # collision with moving into the tile x_axis
        elif self.rect.right + dx >= tile.rect.left - offset_x and (dx < 0 or scrolling):
          dx = 0
          if scrolling:
            offset_x += self.speed
            bg_offset += self.speed
        elif self.rect.left - dx <= tile.rect.right - offset_x and (dx > 0 or scrolling):
          dx = 0
          if scrolling:
            offset_x -= self.speed
            bg_offset -= self.speed

    self.rect.x += dx
    self.rect.y += dy
  def draw(self):
    # animate and draw character
    if self.animation_count > 4 and self.idle == True: # if the animatoin count is greater than the number of frames then reset the frames
      self.animation_count = 1
    elif self.animation_count > 5 and self.moving == True:
      self.animation_count = 1
    if self.idle == True:
      self.image = pygame.image.load('assets/player/idle/Ninja' + str(int(self.animation_count)) + '.png').convert_alpha() # load the image directer with the string form if the integer of the animatoin count for the image frame changes
    else:
      self.image = pygame.image.load('assets/player/running/Ninja' + str(int(self.animation_count)) + '.png').convert_alpha() # load the image directer with the string form if the integer of the animatoin count for the image frame changes
    screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 5, self.rect.y, self.rect.width, self.rect.height))
    self.animation_count += self.animation_speed

# create enemy class
class Enemy(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    self.x = x
    self.y = y
    self.image = pygame.image.load('assets/enemy/enemy.png').convert_alpha()
    self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
    self.vel_y = 20
  def move(self):
    global game_over
    # reset dx
    dx = 0
    dy = 0

    self.vel_y += GRAVITY
    dy += self.vel_y

    if self.rect.centerx + 600 >= player.rect.centerx and self.rect.centerx - 600 <= player.rect.centerx: 
      print('hi')
      if self.rect.top+5 < player.rect.bottom and self.rect.bottom+5 > player.rect.bottom:
        if self.rect.x > player.rect.x:
          dx = -5
        if self.rect.x < player.rect.x:
          dx = 5
    else:
      print('bye')
    for tile in tiles:
      if self.rect.colliderect(tile.rect):
        dy = 0
        self.vel_y = 0
        self.rect.bottom = tile.rect.top
        print('hi')

    if self.rect.top > SCREEN_HEIGHT:
      self.kill()
      enemies.remove(self)
      
    if self.rect.colliderect(player.rect):
      game_over = True

    # move the enemies x positon by dx
    self.x += dx
    self.y += dy
  def draw(self):
    self.rect = pygame.Rect(self.x - offset_x, self.y, 50, 100)
    screen.blit(self.image, (self.rect.x - 20, self.rect.y, self.rect.width, self.rect.height))
    pygame.draw.rect(screen, 'white', self.rect, 2)

class Tile(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    self.x = x
    self.y = y
    self.image = pygame.image.load('assets/tile/grass.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (100,100)).convert_alpha()
    self.rect = pygame.Rect(self.x, self.y, 100, 100)
  def draw(self):
    self.rect = pygame.Rect(self.x - offset_x, self.y, 100, 100)
    screen.blit(self.image, (self.rect.x, self.rect.y, self.rect.width - offset_x, self.rect.height))

def draw_bg():
  screen.blit(bg_image, (0-bg_offset,0))
  screen.blit(bg_image, (SCREEN_WIDTH-bg_offset,0))
  screen.blit(bg_image, (-bg_image.get_width()-bg_offset,0))

def tile_floor(numOfTiles, y):
  for i in range(numOfTiles):
    tiles.append(Tile(i*100, y))

# create an instance of player
player = Player(100, 0)


tiles = []

enemies = []

# draw tileMap
tileMap(Tile,tiles, Enemy, enemies)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if game_over == False:
      draw_bg()
      if bg_offset >= SCREEN_WIDTH:
        bg_offset = 0

      if bg_offset <= -SCREEN_WIDTH:
        bg_offset = 0

      # draw player on the screen
      player.move()
      player.draw()

      # draw tiles
      for tile in tiles:
        tile.draw()
      for e in enemies:
        e.move()
        e.draw()
      print(len(enemies))
    else:
      screen.fill('black')
      draw_text('You lose', font_big, 'white', SCREEN_WIDTH/2- 200, 200)
      draw_text('press w to restart the game', font_big, 'white', SCREEN_WIDTH/2 - 200, 300)
      keys = pygame.key.get_pressed()
      if keys[pygame.K_w]:
        game_over = False
        player.rect.x = 100 - offset_x
        player.rect.y = SCREEN_HEIGHT - 100
        offset_x = 0
        
        tiles.clear()
        for tile in tiles:
          tile.kill()
        enemies.clear()
        for enemy in enemies:
          enemy.kill()
        tileMap(Tile, tiles, Enemy, enemies)
    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
