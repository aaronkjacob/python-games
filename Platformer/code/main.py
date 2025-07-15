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
        self.jump_count = 0
    def jump(self):
        self.y_vel = -self.GRAVITY * 8  # Set vertical velocity for jumping
        self.animation_count = 0  # Reset animation count when jumping
        self.jump_count += 1  # Increment jump count
        if self.jump_count == 1:
            self.fall_count = 0  # Reset fall count when jumping

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
        self.y_vel += min(1, (self.fall_count / fps))  * self.GRAVITY  # Apply gravity
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()  # Update the sprite based on movement and direction

    def landed(self):
        self.fall_count = 0  # Reset fall count when landed
        self.y_vel = 0  # Reset vertical velocity when landed
        self.jump_count = 0  # Reset jump count when landed
    def hit_head(self):
        self.count = 0  # Reset fall count when hit head
        self.y_vel *= -1  # Reverse vertical velocity when hit head
    
    def update_sprite(self):
        sprite_sheet = 'idle'
        if self.y_vel < 0:  # If jumping
            if self.jump_count == 1:
                sprite_sheet = 'jump'
            elif self.jump_count == 2:
                sprite_sheet = 'double_jump'
        elif self.y_vel > self.GRAVITY * 2:  # If falling
            sprite_sheet = 'fall'
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
    def draw(self, screen, offset_x):
        screen.blit(self.sprite, (self.rect.x-offset_x, self.rect.y))  # Draw the player
        self.mask = pygame.mask.from_surface(self.sprite)  # Create a mask from the sprite for collision detection

class Object(pygame.sprite.Sprite):
    def __init__(self, x,y,width,height,name=None):
        #super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    def draw(self, screen, offset_x):
        screen.blit(self.image, (self.rect.x-offset_x, self.rect.y))  # Draw the object on the screen
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

def draw(screen,background, bg_image, player, Objects,offset_x):
    for tile in background:
        screen.blit(bg_image, tile)
    for obj in Objects:
        obj.draw(screen, offset_x)  # Draw each object on the screen with offset
    pygame.display.update()
    player.draw(screen, offset_x)  # Draw the player on the screen



def handle_vertical_collision(player, objects,dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_rect(player,obj): # Check for collision using masks
            if dy > 0:  # Moving down
                player.rect.bottom = obj.rect.top  # Set player bottom to object top
                player.landed()
            elif dy < 0:  # Moving up
                player.rect.top = obj.rect.bottom # Set player top to object bottom
                player.hit_head()
        collided_objects.append(obj)  # Add collided objects to the list
    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0)  # Move player horizontally
    player.update()  # Update player rect position
    collided_objects = []  # List to store collided objects
    for obj in objects:
        if pygame.sprite.collide_rect(player, obj):
            collided_objects = obj
            break
    player.move(-dx, 0)  # Move player back to original position
    player.update()  # Update player rect position
    return collided_objects  # Return the first collided object



def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0  # Reset horizontal velocity

    collide_left = collide(player, objects, -PLAYER_VELOCITY * 2)  # Check for collision when moving left
    collide_right = collide(player, objects, PLAYER_VELOCITY * 2)  # Check for collision when moving right

    if keys[pygame.K_LEFT] and not collide_left:  # If left key is pressed and no collision
        player.move_left(PLAYER_VELOCITY)
    if keys[pygame.K_RIGHT] and not collide_right:  # If right key is pressed and no collision
        player.move_right(PLAYER_VELOCITY)

    handle_vertical_collision(player, objects, player.y_vel)  # Handle vertical collisions

def main(screen):
    clock = pygame.time.Clock() # Initialize the clock

    background, bg_image = get_background("Yellow.png")  # Load the background image

    block_size = 96

    player = Player(100, 100, 50, 50)  # Create a player instance
    floor = [Block(i*block_size, SCREEN_HEIGHT - block_size, block_size) for i in range(-SCREEN_WIDTH // block_size, SCREEN_WIDTH*2 // block_size)]  # Create a floor of blocks
    objects = [*floor, Block(0,SCREEN_HEIGHT - block_size * 2, block_size), Block(block_size * 3, SCREEN_HEIGHT - block_size * 4, block_size)]  # Create some additional blocks

    offset_x = 0
    scroll_area_width = 200  # Width of the scroll area

    running = True # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE:  # Check if space key is pressed
                    if player.jump_count < 2:
                        player.jump()

        player.loop(FPS)  # Update player position
        handle_move(player, objects) # Handle player movement
        # Fill the screen with the background color
        draw(screen,background,bg_image, player, objects, offset_x)  # Draw the background and player

        if (player.rect.right - offset_x >= SCREEN_WIDTH - scroll_area_width and player.x_vel > 0) or (
            player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0):
            offset_x += player.x_vel



        # Update the display
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main(screen)

