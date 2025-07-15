import pygame
import os
import math
import random
from os import listdir
from os.path import isfile, join


# Initialize Pygame
pygame.init()

# Set up window dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

BG_COLOR = ('white')  # White background
FPS = 60  # Frames per second

PLAYER_VELOCITY = 5  # Player movement speed

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites] # Flip sprites horizontally
def load_spritesheet(dir1,dr2,width,height,direction=False):
    path = join("Platformer", "assets", dir1, dr2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        if direction:
            all_sprites[image.replace('.png','') + '_right'] = sprites
            all_sprites[image.replace('.png','') + '_left'] = flip(sprites)
        else:
            all_sprites[image.replace('.png','')] = sprites
    return all_sprites

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)  # Player color (red)
    GRAVITY = 1
    SPRITES = load_spritesheet("MainCharacters", "MaskDude", 32, 32, True) # Load player spritesheet

    def __init__(self, x,y,width,height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = 'left'
        self.animation_count = 0
        self.fall_count = 0
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != 'left':
            self.direction = 'left'
            self.animation_count - 0
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != 'right':
            self.direction = 'right'
            self.animation_count = 0
    def loop(self,fps):
        #self.y_vel += min(1, (self.fall_count / fps))  * self.GRAVITY  # Apply gravity
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
    def draw(self, screen):
        self.sprite = self.SPRITES["idle_" + self.direction][0] # Default sprite
        screen.blit(self.sprite, (self.rect.x, self.rect.y))  # Draw the player sprite


def get_background(name):
    # Load background image
    image = pygame.image.load(join("Platformer","assets", "Background", name))
    __, __, width, height = image.get_rect()
    tiles = []

    for i in range(SCREEN_WIDTH // width + 1):
        for j in range(SCREEN_HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image

def draw(screen,background, bg_image, player):
    for tile in background:
        screen.blit(bg_image, tile)
    pygame.display.update()
    player.draw(screen)  # Draw the player on the screen

def handle_move(player):
    keys = pygame.key.get_pressed()
    player.x_vel = 0  # Reset horizontal velocity
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VELOCITY)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VELOCITY)

    player.loop(FPS)  # Update player position

def main(screen):
    clock = pygame.time.Clock() # Initialize the clock

    background, bg_image = get_background("Yellow.png")  # Load the background image

    player = Player(100, 100, 50, 50)  # Create a player instance

    running = True # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        player.loop(FPS)  # Update player position
        handle_move(player) # Handle player movement
        # Fill the screen with the background color
        draw(screen,background,bg_image, player)



        # Update the display
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main(screen)

