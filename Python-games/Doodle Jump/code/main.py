#import necessary modules
import pygame

# Initialize Pygame
pygame.init()

# Set up window dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumpy")

# Running variable and clock
clock = pygame.time.Clock()
running = True

# load images
jumpy_image = pygame.image.load('Python-games/Doodle Jump/Assets/jump.png')

bg_image = pygame.image.load('Python-games/Doodle Jump/Assets/bg.png').convert_alpha() # Background Image

# Player class
class Player():
    def __init__(self, x, y):
        self.image = jumpy_image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def draw(self):
        screen.blit(self.image, self.rect)

jumpy = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT - 150)

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (e.g., black)
    screen.fill((0, 0, 0))

    # Draw background
    screen.blit(bg_image, (0,0,SCREEN_WIDTH, SCREEN_HEIGHT))

    # Draw player
    jumpy.draw()

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()