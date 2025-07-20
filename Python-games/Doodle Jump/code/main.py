#import necessary modules
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up window dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumpy")

# Running variable and clock
clock = pygame.time.Clock()
FPS = 60
running = True

# Game variables
GRAVITY = 1
MAX_PLATFORMS = 10

# load images
jumpy_image = pygame.image.load('Python-games/Doodle Jump/Assets/jump.png').convert_alpha()
bg_image = pygame.image.load('Python-games/Doodle Jump/Assets/bg.png').convert_alpha() # Background Image
platform_image = pygame.image.load('Python-games/Doodle Jump/Assets/wood.png').convert_alpha()

# Player class
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(jumpy_image, (45, 45))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)
        self.vel_y = 0
        self.flip = False
    def move(self):
        #reset moving variables
        dx = 0
        dy = 0

        #process keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            dx = -10
            self.flip = True
        if key[pygame.K_d]:
            dx = 10
            self.flip = False

        # Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player doesn't leave the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0
            self.vel_y = -20

        # update rec pos
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))
        pygame.draw.rect(screen, 'black', self.rect, 2)

# platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# player instance
jumpy = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT - 150)

# Platform group
platform_group = pygame.sprite.Group()

# create temporary platforms
for p in range(MAX_PLATFORMS):
    p_w = random.randint(40,60)
    p_x = random.randint(0,SCREEN_WIDTH-p_w)
    p_y = p * random.randint(80,120)
    platform = Platform(p_x,p_y,p_w)
    platform_group.add(platform)


# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., black)
    screen.fill((0, 0, 0))

    # Draw background
    screen.blit(bg_image, (0,0,SCREEN_WIDTH, SCREEN_HEIGHT))

    platform_group.draw(screen)

    # Draw player
    jumpy.move()
    jumpy.draw()

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()