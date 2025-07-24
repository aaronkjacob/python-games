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
bg_image = pygame.image.load('Python-games/Solo-projects/Ninja-platformer/assets/background.png').convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT+260))

# game variables
GRAVITY = 1
offset_x = 0


# player class
class Player(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    self.x = x
    self.y = y
    self.animation_count = 1
    self.animage_frame = [0,1,2,3]
    self.image = pygame.image.load('Python-games/Solo-projects/Ninja-platformer/assets/player/idle/Ninja1.png').convert_alpha()
    self.rect = pygame.Rect(x,y,self.image.get_width(),self.image.get_height())
    self.speed = 10
    self.flip = True
    self.jump_count = 0
    self.vel_y = 0
    self.animation_speed = .1
    self.idle = True
    self.moving = False
  def move(self):
    global offset_x
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
      self.vel_y = -20
      self.jump_count += 1


    # collision with bottom wall
    if self.rect.bottom + dy >= SCREEN_HEIGHT and dy > 0:
      dy = 0
      self.jump_count = 0
      self.rect.bottom = SCREEN_HEIGHT

    if self.rect.right > SCREEN_WIDTH-400 and dx > 0:
      dx = 0
      offset_x += self.speed
    if self.rect.left < 400 and dx < 0:
      dx = 0
      offset_x -= self.speed

    # collision with tile
    for tile in tiles:
      if self.rect.colliderect(tile.rect):
        if dy > 0 and self.vel_y > 0:
          dy = .5
          self.vel_y = 0
          self.jump_count = 0
          self.rect.bottom = tile.rect.top
        elif self.rect.right + dx >= tile.rect.left - offset_x and dx < 0:
          dx = 0
        elif self.rect.left - dx <= tile.rect.right - offset_x and dx > 0:
          dx = 0

      


    self.rect.x += dx
    self.rect.y += dy
  def draw(self):
    # animate and draw character
    if self.animation_count > 4 and self.idle == True: # if the animatoin count is greater than the number of frames then reset the frames
      self.animation_count = 1
    elif self.animation_count > 5 and self.moving == True:
      self.animation_count = 1
    if self.idle == True:
      self.image = pygame.image.load('Python-games/Solo-projects/Ninja-platformer/assets/player/idle/Ninja' + str(int(self.animation_count)) + '.png').convert_alpha() # load the image directer with the string form if the integer of the animatoin count for the image frame changes
    else:
      self.image = pygame.image.load('Python-games/Solo-projects/Ninja-platformer/assets/player/running/Ninja' + str(int(self.animation_count)) + '.png').convert_alpha() # load the image directer with the string form if the integer of the animatoin count for the image frame changes
    screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    pygame.draw.rect(screen, 'white', self.rect, 2)
    self.animation_count += self.animation_speed

class Tile(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    self.x = x
    self.y = y
    self.image = pygame.image.load('C:/Users/aaron/OneDrive/Desktop/All My code/python-code/Python-games/Solo-projects/Ninja-platformer/assets/grass.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (100,100))
    self.rect = pygame.Rect(self.x, self.y, 100, 100)
  def draw(self):
    self.rect = pygame.Rect(self.x - offset_x, self.y, 100, 100)
    screen.blit(self.image, (self.rect.x, self.rect.y, self.rect.width - offset_x, self.rect.height))

def draw_bg():
  screen.blit(bg_image, (0-offset_x,0))
  screen.blit(bg_image, (SCREEN_WIDTH-offset_x,0))
  screen.blit(bg_image, (-bg_image.get_width()-offset_x,0))

# create an instance of player
player = Player(SCREEN_WIDTH/2, 0)

tiles = []


tiles.append(Tile(SCREEN_WIDTH/2, SCREEN_HEIGHT-97))



# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_bg()
    if offset_x >= SCREEN_WIDTH:
      offset_x = 0

    if offset_x <= -SCREEN_WIDTH:
      offset_x = 0

    # draw player on the screen
    player.move()
    player.draw()

    # draw tiles
    for tile in tiles:
      tile.draw()


    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
