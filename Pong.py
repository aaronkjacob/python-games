import pygame
import time
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Paddle variables
paddleSpeed = 15

# Ball color
ballColor = ['white','red','green','purple',]
print(ballColor)

class Paddle():
  def __init__(self,x,y,width,height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.rect = pygame.Rect(x,y,width,height)

    self.score = 0
  def draw(self):
    pygame.draw.rect(screen, 'white', self.rect)
  def move(self,dx,dy):
    self.x += dx
    self.y += dy
    self.rect.topleft = (self.x, self.y)
  def wallCollision(self):
    if self.y <= -10:
      self.y += paddleSpeed
    elif self.y + self.height >= screen.get_height()+10:
      self.y -= paddleSpeed

class Ball():
  def __init__(self,x,y,radius,ballSpeed):
    self.x = x
    self.y = y
    self.radius = radius
    self.ball_x_speed = ballSpeed
    self.ball_y_speed = ballSpeed
    self.wait = True
    self.initialV_X = random.randint(1,2)
    self.initialV_Y = random.randint(1,2)
    self.color = 'white'
  def draw(self):
    # Draw
    self.circle = pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)
  def collisionWithWall(self):
    # Top and bottom wall collision
    if self.y+self.radius >= screen.get_height():
      self.ball_y_speed = -self.ball_y_speed
    elif self.y-self.radius <= 0:
      self.ball_y_speed = -self.ball_y_speed
    # Right and left wall collision
    if self.x+self.radius >= screen.get_width():
      self.x = screen.get_width()/2
      self.y = screen.get_height()/2
      paddleA.score += 1
      self.ball_x_speed = 5
      self.ball_y_speed = 5
      self.wait = True
      self.initialV_X = random.randint(1,2)
      self.initialV_Y = random.randint(1,2)

    if self.x-self.radius <= 0:
      self.x = screen.get_width()/2
      self.y = screen.get_height()/2
      paddleB.score += 1
      self.ball_x_speed = 5
      self.ball_y_speed = 5
      self.wait = True
      self.initialV_X = random.randint(1,2)
      self.initialV_Y = random.randint(1,2)

  def collisionWithPaddle(self):
    # Collision with the Paddle
    if (self.x+self.radius > paddleB.x) and (self.y >= paddleB.y and self.y <= (paddleB.y + paddleB.height)):
      self.ball_x_speed = -self.ball_x_speed
      if self.ball_x_speed > 0:
        self.ball_x_speed += 1
        print(self.ball_x_speed)
      elif self.ball_x_speed < 0:
        self.ball_x_speed -= 1
        print(self.ball_x_speed)

      if self.ball_y_speed > 0:
        self.ball_y_speed += .5
        print(self.ball_y_speed)
      elif self.ball_y_speed < 0:
        self.ball_y_speed -= .5
        print(self.ball_y_speed)

    if (self.x-self.radius < (paddleA.x + paddleA.width)) and (self.y >= paddleA.y and self.y <= (paddleA.y + paddleA.height)):
      self.ball_x_speed = -self.ball_x_speed
      if self.ball_x_speed > 0:
        self.ball_x_speed += 1
        print(self.ball_x_speed)
      elif self.ball_x_speed < 0:
        self.ball_x_speed -= 1
        print(self.ball_x_speed)

      if self.ball_y_speed > 0:
        self.ball_y_speed += .5
        print(self.ball_y_speed)
      elif self.ball_y_speed < 0:
        self.ball_y_speed -= .5
        print(self.ball_y_speed)


  def move(self):
    if self.initialV_X == 1:
      self.x += self.ball_x_speed
    elif self.initialV_X == 2:
      self.x -= self.ball_x_speed
    if self.initialV_Y == 1:
      self.y += self.ball_y_speed

    elif self.initialV_Y:
      self.y -= self.ball_y_speed

    self.circle

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
 
paddleA = Paddle(10,screen.get_height()/2-90,10,180)
paddleB = Paddle(screen.get_width()-20,screen.get_height()/2-90,10,180)

ball = Ball(screen.get_width()/2, screen.get_height()/2,10,5)



while running:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
  keys = pygame.key.get_pressed()
  # Movment for Paddle A
  if keys[pygame.K_w]:
    paddleA.move(0,-paddleSpeed)
  if keys[pygame.K_s]:
    paddleA.move(0,paddleSpeed)

  # Movment for Paddle B
  if keys[pygame.K_UP]:
    paddleB.move(0,-paddleSpeed)
  if keys[pygame.K_DOWN]:
    paddleB.move(0,paddleSpeed)

  # Stop window shortcut
  if keys[pygame.K_BACKSPACE]:
    running = False
  elif keys[pygame.K_ESCAPE]:
    running = False

  screen.fill('black')

  paddleA.draw()
  paddleB.draw()
  paddleA.wallCollision()
  paddleB.wallCollision()

  if ball.ball_x_speed >= 15:
    ball.ball_x_speed -= 1
  
  if ball.ball_y_speed >= 10:
    ball.ball_y_speed -= 1


  # This is to create, move and track collsion for the ball
  ball.draw()
  ball.move()
  ball.collisionWithWall()
  ball.collisionWithPaddle()

  scoreStr = str(paddleA.score) + ':' + str(paddleB.score)
  score = Text(scoreStr,70,(screen.get_width()/2,100))
  score.draw()

  pygame.display.update()
  clock.tick(60)

  # If the game starts or restarts then this if statemants makes the ball wait 1 second to move
  if ball.wait:
    time.sleep(1)
    ball.wait = False


pygame.quit()