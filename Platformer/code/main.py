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

def get_block(size):
    path = join("Platformer", "assets", "Terrain",  "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)  # Scale the block image to double its size

class Player(pygame.sprite.Sprite):
    #super().__init__()
    COLOR = (255, 0, 0)  # Player color (red)
    GRAVITY = 1
    SPRITES = load_spritesheet("MainCharacters", "MaskDude", 32, 32, True) # Load player spritesheet
    ANIMATION_DELAY = 3

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
        self.update_sprite()  # Update the sprite based on movement and direction

    def update_sprite(self):
        sprite_sheet = 'idle'
        if self.x_vel != 0:  # If moving, use walking animation
            sprite_sheet = 'run'
        sprite_sheet_name = sprite_sheet + '_' + self.direction
        sprites = self.SPRITES[sprite_sheet_name] # Get the appropriate sprite sheet based on direction
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites) # Calculate the current sprite index based on animation count
        self.sprite = sprites[sprite_index]  # Get the current sprite based on animation count
        self.animation_count += 1  # Increment animation count for next frame
        self.update()  # Update the rect position based on sprite
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))  # Update the rect position based on sprite
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))  # Draw the player
        self.mask = pygame.mask.from_surface(self.sprite)  # Create a mask from the sprite for collision detection

class Object(pygame.sprite.Sprite):
    def __init__(self, x,y,width,height,name=None):
        #super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))  # Draw the object on the screen
class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0,0)) # Load the block image and draw it on the object surface
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask from the block image for collision detection

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

def draw(screen,background, bg_image, player, Objects):
    for tile in background:
        screen.blit(bg_image, tile)
    for obj in Objects:
        obj.draw(screen)
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

    block_size = 96

    player = Player(100, 100, 50, 50)  # Create a player instance
    floor = [Block(i*block_size, SCREEN_HEIGHT - block_size, block_size) for i in range(-SCREEN_WIDTH // block_size, SCREEN_WIDTH*2 // block_size)]  # Create a floor of blocks

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
        draw(screen,background,bg_image, player, floor)



        # Update the display
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main(screen)

