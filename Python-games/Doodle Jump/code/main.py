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
SCROLL_THRESHOLD = 200
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0

# define font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

# load images
jumpy_image = pygame.image.load('Python-games/Doodle Jump/Assets/jump.png').convert_alpha()
bg_image = pygame.image.load('Python-games/Doodle Jump/Assets/bg.png').convert_alpha() # Background Image
platform_image = pygame.image.load('Python-games/Doodle Jump/Assets/wood.png').convert_alpha()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

# function for drawing the background
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0,0+bg_scroll))
    screen.blit(bg_image, (0,-600+bg_scroll))

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
        scroll = 0
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
        
        # Check collision with platform
        for platform in platform_group:
            #collision in the y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20

        # check if the player has bounced to the top of the screen
        if self.rect.top <= SCROLL_THRESHOLD:
            if self.vel_y < 0:
                scroll = -dy

        # update rec pos
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

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
    def update(self, scroll):
        # update platform's vertical positoin
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            platform_group.remove(self)

# player instance
jumpy = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT - 150)

# Platform group
platform_group = pygame.sprite.Group()

# create starting platform
platform = Platform((SCREEN_WIDTH / 2) - 50, SCREEN_HEIGHT-100,100)
platform_group.add(platform)


# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game_over == False:

        # Draw background
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_bg(bg_scroll)

        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40,60)
            p_x = random.randint(0, SCREEN_WIDTH-p_w)
            p_y = platform.rect.y -random.randint(90,125)
            platform = Platform(p_x, p_y,p_w)
            platform_group.add(platform)

        # update platforms
        platform_group.update(scroll)
        platform_group.draw(screen)

        # Draw player
        scroll = jumpy.move()
        jumpy.draw()

        # check game over
        if jumpy.rect.top > SCREEN_HEIGHT:
            game_over = True
    else:
        if game_over == True:
            screen.fill('black')
            draw_text('GAME OVER!', font_big, 'white', 130, 200)
            draw_text('SCORE: ' + str(score), font_small, 'white', 130,400)
            draw_text('PRESS SPACE TO PLAY AGAIN', font_big, 'white', 40, 300)
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                game_over = False
                # reset variables
                score = 0
                scroll = 0

                # reset jumpy
                jumpy.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 150)
                platform_group.empty()

                #create starting platform

                platform = Platform((SCREEN_WIDTH / 2) - 50, SCREEN_HEIGHT-100,100)
                platform_group.add(platform)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()