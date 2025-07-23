import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Road Rush")

# road image
road_image = pygame.image.load('Python-games/Solo-projects/Road-rush/assets/road.png').convert_alpha()
road_image = pygame.transform.scale(road_image, (SCREEN_WIDTH,SCREEN_HEIGHT))

# game over variable
game_over = False

# score variable
score = 0
high_score = 0

class Player(pygame.sprite.Sprite): 
  def __init__(self, x, y):
    super().__init__()
    self.x = x
    self.y = y
    self.x_speed = 10
    self.starting_speed = 10
    self.y_speed = self.starting_speed
    self.image = pygame.image.load('Python-games/Solo-projects/Road-rush/assets/motor-bike.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (100,100))
    self.rect = pygame.Rect(self.x,self.y,80,100)
  def move(self):
    dx = 0
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        dx = -self.x_speed
    if key[pygame.K_d]:
        dx = self.x_speed
    if key[pygame.K_w]:
      self.y_speed = self.y_speed + 1/20
    else:
      self.y_speed = self.starting_speed

    # check for collision with the wall
    if player.rect.right + dx >= SCREEN_WIDTH - 30:
      dx = 0
    if player.rect.left + dx <= 25:
      dx = 0

    
    self.rect.x += dx

  def draw(self):
    screen.blit(self.image, (self.rect.x-10,self.rect.y,self.rect.width,self.rect.height))

class Obstacle(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    lane = random.randint(1,4)
    if lane == 1:
      self.x = 50
    if lane == 2:
      self.x = 240
    if lane == 3:
      self.x = 430
    if lane == 4:
      self.x = 625
    
    self.y = -300

    image = random.randint(1,6)
    if image == 1:
      self.image = pygame.image.load('Python-games/Solo-projects/Road-rush/assets/blue-car.png').convert_alpha()
    if image == 2:
      self.image = pygame.image.load('Python-games/Solo-projects/Road-rush/assets/red-pickup-truck.png').convert_alpha()
    if image == 3:
      self.image = pygame.image.load('Python-games/Solo-projects/Road-rush/assets/red-semi-truck.png').convert_alpha()
    if image == 4:
      self.image = pygame.image.load('Python-games/Solo-projects/Road-rush/assets/yellow-car.png').convert_alpha()
    if image == 5:
      self.image = pygame.image.load('Python-games/Solo-projects/Road-rush/assets/yellow-pickup-truck.png').convert_alpha()
    if image == 6:
      self.image = pygame.image.load('Python-games/Solo-projects/Road-rush/assets/yellow-semi-truck.png').convert_alpha()
   
    self.image = pygame.transform.scale(self.image, (200,200))
    self.image = pygame.transform.flip(self.image, False, True)
    self.rect = pygame.Rect((self.x, self.y, 120,200))
    self.speed = random.randint(int(player.y_speed-10),int(player.y_speed-5))
  def move(self):
    self.rect.y += self.speed + player.y_speed
    if self.rect.top > SCREEN_HEIGHT:
      self.kill()
      obstacle_group.remove(self)
  def draw(self):
    screen.blit(self.image, (self.rect.x-40,self.rect.y,self.rect.width,self.rect.height))

# create player instance
player = Player(SCREEN_WIDTH/2 - 43, SCREEN_HEIGHT-150)

obstacle_group = []

obstacle_group.append(Obstacle())

road_scroll = 0

def draw_bg(road_scroll):
  screen.blit(road_image, (0,road_scroll))
  screen.blit(road_image, (0,road_scroll-SCREEN_HEIGHT))

# make font variable
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x,y))

# Set up clock
clock = pygame.time.Clock()
FPS = 60



# Main game loop
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False


  if game_over == False:
    # draw background
    draw_bg(road_scroll)
    road_scroll += player.y_speed
    if road_scroll >= SCREEN_HEIGHT:
      road_scroll = 0

    # write the score on the screen
    draw_text(str(int(score)), font_big, 'red', SCREEN_WIDTH/2-20,100)

    # move and draw player
    player.move()
    player.draw()


    for obstacle in obstacle_group:
      # check for collision with the player for every obstacle
      if obstacle.rect.colliderect(player.rect):
        game_over = True
        player.kill()
        obstacle_group.clear()
      # move and draw obstacles
      obstacle.move()
      obstacle.draw()
    # if there are less than 3 obstacles then make a new one
    if len(obstacle_group) < 3:
      obstacle_group.append(Obstacle())

    # increase the score
    score += 1

    if score>=high_score:
      high_score = score


  else:
    # what happens when you die
    screen.fill('black')
    if game_over == True:
        screen.fill('black')
        draw_text('GAME OVER!', font_big, 'white', SCREEN_WIDTH/2-60, 200)
        draw_text('SCORE: ' + str(int(score)), font_big, 'white', SCREEN_WIDTH/2-40, 400)
        draw_text('HIGH SCORE: ' + str(int(high_score)), font_big, 'white', SCREEN_WIDTH/2-40, 500)
        draw_text('PRESS SPACE TO PLAY AGAIN', font_big, 'white', SCREEN_WIDTH/2-180, 300)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_over = False
            score = 0


  # Update the display
  pygame.display.flip()
  clock.tick(FPS)

pygame.quit()
sys.exit()
