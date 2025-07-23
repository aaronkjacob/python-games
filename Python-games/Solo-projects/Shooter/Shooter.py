import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1200, 800  # Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Setup Example")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
      self.width = width
      self.height = height
      self.x = x-(self.width/2)
      self.y = y-(self.height/2)
      self.score = 0
      self.incScore = 0

      self.speed = 8
      self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
      self.surf = pygame.surface.Surface((self.rect.width,self.rect.height))
      self.surf.fill('red')
    def main(self):
      screen.blit(self.surf, self.rect)

class PlayerBullet(pygame.sprite.Sprite):
  def __init__(self, x, y ,mouse_x,mouse_y):
    self.x = x
    self.y = y
    self.mouse_x = mouse_x
    self.mouse_y = mouse_y
    self.speed = 15
    self.radius = 10
    self.angle = math.atan2(y-mouse_y,x-mouse_x)
    self.x_vel = math.cos(self.angle) * self.speed
    self.y_vel = math.sin(self.angle) * self.speed

  def main(self):
    if (len(player_bullets) >= 0):
      self.x -= int(self.x_vel)
      self.y -= int(self.y_vel)
      pygame.draw.circle(screen, 'black', (self.x, self.y), self.radius)

    if self.x > WIDTH+50:
      player_bullets.remove(self)
    elif self.x < -50:
      player_bullets.remove(self)

    if self.y > HEIGHT+50:
      player_bullets.remove(self)
    elif self.y < -50:
      player_bullets.remove(self)

class enemy(pygame.sprite.Sprite):
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.speed = random.randint(5000,10000)/3000
    self.size = 30
    self.spawnSide = random.randint(1,4)
    self.rect = pygame.Rect(self.x-screen_scroll[0],self.y-screen_scroll[1],self.size,self.size)

  def spawn(self):
    
    if self.spawnSide == 1:
      self.y = -1800
      self.x = random.randint(0,1500)
    if self.spawnSide == 4:
      self.y = 1800
      self.x = random.randint(0,1500)

    if self.spawnSide == 3:
      self.y = random.randint(0,1500)
      self.x = -1800
    if self.spawnSide == 2:
      self.y = random.randint(0,1500)
      self.x = 1800


  def main(self):
    pygame.draw.rect(screen, 'white', self.rect)
    self.rect = pygame.Rect(self.x-screen_scroll[0],self.y-screen_scroll[1],self.size,self.size)
    if self.x < player.x + screen_scroll[0]:
      self.x += self.speed + random.randint(0,2)
    elif self.x > player.x + screen_scroll[0]:
      self.x -= self.speed + random.randint(0,2)

    if self.y < player.y + screen_scroll[1]:
      self.y += self.speed
    elif self.y > player.y + screen_scroll[1]:
      self.y -= self.speed
  def speedIncrease(self,speedIncrease):
    self.speed += speedIncrease

class Text():
  def __init__(self,text,fontSize,coordinates):
    self.text = text
    self.fontSize = fontSize
    self.coordinates = coordinates
    self.font = pygame.font.Font(None, fontSize)
  def draw(self):
    text = self.font.render(self.text, True, 'white')
    text_rect = text.get_rect(center=(self.coordinates))
    screen.blit(text, text_rect)

def background():
  background_rect = pygame.Rect(0,0,WIDTH,HEIGHT)
  background_surf = pygame.image.load('Python-games/Solo-projects/Shooter/background.png').convert_alpha()
  screen.blit(background_surf,(background_rect.x-screen_scroll[0],background_rect.y-screen_scroll[1]))


  backgroundQ2 = [0,1,2,3]
  backgroundQ4 = [0,-1,-2,-3]
  backgroundQ1 = [0,1,2,3]
  backgroundQ3 = [0,-1,-2,-3]

  # This keeps drawing backgrounds in each quadrant
  for i in backgroundQ2:
    for e in backgroundQ2:
      screen.blit(background_surf,(background_rect.x-screen_scroll[0]+(i*500),background_rect.y-screen_scroll[1]+(e*500)))

  for i in backgroundQ4:
    for e in backgroundQ4:
      screen.blit(background_surf,(background_rect.x-screen_scroll[0]+(i*500),background_rect.y-screen_scroll[1]+(e*500)))

  for i in backgroundQ1:
    for e in backgroundQ1:
      screen.blit(background_surf,(background_rect.x-screen_scroll[0]+(i*500),background_rect.y-screen_scroll[1]+(e*-500)))

  for i in backgroundQ3:
    for e in backgroundQ3:
      screen.blit(background_surf,(background_rect.x-screen_scroll[0]+(i*500),background_rect.y-screen_scroll[1]+(e*-500)))
  
  length = len(backgroundQ1) -1
  if screen_scroll[0] >= length*500:
    screen_scroll[0] -= player.speed

  if screen_scroll[0] <= -length*500 - 350:
    screen_scroll[0] += player.speed

  if screen_scroll[1] >= length*500:
    screen_scroll[1] -= player.speed

  if screen_scroll[1] <= -length*500 - 250:
    screen_scroll[1] += player.speed




# Set up clock for controlling frame rate
clock = pygame.time.Clock()

player = Player(WIDTH/2,HEIGHT/2,32,32)

screen_scroll = [0,0]

player_bullets = []

enemies = []

  


enemy_count = [1,1,1,1,1,1,1,1,1,1,1,1] 
for e in enemy_count:
  enemies.append(enemy((random.randint(-100,0)),(random.randint(-100,0))))

increase = False



# Main game loop
running = True
while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:  # Handle window close
          running = False
      if event.type == pygame.MOUSEBUTTONDOWN:
         if event.button == 1:
            player_bullets.append(PlayerBullet(player.rect.centerx, player.rect.centery, mouse_x, mouse_y))

    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
       screen_scroll[0] -= player.speed
       for bullet in player_bullets:
          bullet.x += 5
    if keys[pygame.K_d]:
       screen_scroll[0] += player.speed
       for bullet in player_bullets:
          bullet.x -= 5
    if keys[pygame.K_w]:
       screen_scroll[1] -= player.speed
       for bullet in player_bullets:
          bullet.y += 5
    if keys[pygame.K_s]:
       screen_scroll[1] += player.speed
       for bullet in player_bullets:
          bullet.y -= 5
    
    if keys[pygame.K_BACKSPACE]:
      sys.exit()
      pygame.quit()
      running = false


    # Drawing code
    screen.fill('black')
    background()
    
    score = Text("score:"+str(player.score), 50, (WIDTH/2,60))
    score.draw()

    print(len(player_bullets))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    player.main()

    for bullet in player_bullets:
      bullet.main()
    for e in enemies:
      e.main()
      if e.rect.colliderect(player.rect):
        sys.exit()
        pygame.quit()
        running = false
      if e.rect.colliderect(e.rect):
        pass
      for bullets in player_bullets:
        if e.rect.collidepoint(bullet.x,bullet.y):
          e.spawn()
          player.score += 1
          player.incScore
        
      # increase enemy speed
      if player.incScore >= 3000:
        increase = True
        player.incScore = 0
      if increase == True:
        enemies.append(enemy((random.randint(-100,0)),(random.randint(-100,0))))
        increase = False
      #
      
    pygame.display.update()  # Update the display

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()