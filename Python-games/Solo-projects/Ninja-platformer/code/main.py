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
    self.animation_count = 1
    self.animage_frame = [0,1,2,3]
    self.image = pygame.image.load('Python-games/Solo-projects/Ninja-platformer/assets/player/idle/Ninja1.png')
    self.rect = pygame.Rect(x,y,self.image.get_width(),self.image.get_height())
    self.speed = 10
    self.flip = True
    self.jump_count = 0
    self.vel_y = 0
    self.animation_speed = .1
    self.idle = True
    self.moving = False
  def move(self):
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

    self.rect.x += dx
    self.rect.y += dy
  def draw(self):
    # animate and draw character
    if self.animation_count > 4: # if the animatoin count is greater than the number of frames then reset the frames
      self.animation_count = 1
    if self.idle == True:
      self.image = pygame.image.load('Python-games/Solo-projects/Ninja-platformer/assets/player/idle/Ninja' + str(int(self.animation_count)) + '.png') # load the image directer with the string form if the integer of the animatoin count for the image frame changes
    else:
      self.image = pygame.image.load('Python-games/Solo-projects/Ninja-platformer/assets/player/idle/Ninja1.png')
    screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    pygame.draw.rect(screen, 'white', self.rect, 2)
    self.animation_count += self.animation_speed

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
