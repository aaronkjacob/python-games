import pygame
import os
import math
import random
from os import listdir
from os.path import isfile, join

def tiles():
    def tile_floor(num, x, y):
        for i in range(num):
            objects.append(Block(x+block_size*i, y, block_size))
    global objects
    def draw_fire(x, y):
        global fire

        fire = Fire(x, y, 16, 32)
        fire.on()
        objects.append(fire)

        
    block_size = 96
    objects = []  # Create some additional blocks


    tile_floor(5, 0,SCREEN_HEIGHT-block_size)
    draw_fire(300, 600)

    tile_floor(3, 700, SCREEN_HEIGHT - 200)

    tile_floor(2, 1200, 500)

    tile_floor(1, 1700, 350)

    tile_floor(3, 2000, 700)




# Initialize Pygame
pygame.init()

# Set up window dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

BG_COLOR = ('white')  # White background
FPS = 60  # Frames per second

# game variables
PLAYER_VELOCITY = 5  # Player movement speed
game_over = False
menu_screen = True

# make font variable
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x,y))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites] # Flip sprites horizontally
def load_spritesheet(dir1,dr2,width,height,direction=False):
    path = join("assets", dir1, dr2)
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
    path = join("assets", "Terrain",  "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)  # Scale the block image to double its size

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)  # Player color (red)
    GRAVITY = 1
    SPRITES = load_spritesheet("MainCharacters", "NinjaFrog", 32, 32, True) # Load player spritesheet
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
        self.hit = False  # Flag to check if player is hit
        self.hit_count = 0  # Counter for hit animation
    def make_hit(self):
        self.hit = True
        self.hit_count = 0
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

        if self.hit: # If player is hit, apply hit animation
            self.hit_count += 1
        if self.hit_count >= fps * 2:
            self.hit = False
            self.hit_count = 0 # Reset hit count after hit animation

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
        if self.hit:  # If player is hit, use hit animation
            sprite_sheet = 'hit'
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
class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y + 40, width, height, "fire")
        self.fire = load_spritesheet("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

def get_background(name):
    # Load background image
    image = pygame.image.load(join("assets", "Background", name))
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

    if keys[pygame.K_a] and not collide_left:  # If left key is pressed and no collision
        player.move_left(PLAYER_VELOCITY)
    if keys[pygame.K_d] and not collide_right:  # If right key is pressed and no collision
        player.move_right(PLAYER_VELOCITY)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)  # Handle vertical collisions
    to_check = [collide_left, collide_right, *vertical_collide]  # List of objects to check for collisions
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()  # If player collides with fire, set hit flag

# Font setup
font = pygame.font.Font(None, 36)


# Button function
def draw_button(screen, color, x, y, width, height, text=''):
    global menu_screen
    button_rect = pygame.draw.rect(screen, color, (x, y, width, height))
    if text:
        text_surface = font.render(text, True, 'black')
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(pos[0], pos[1]):
            menu_screen = False
            

def menu():
    screen.fill('black')
    for i in range(1,5):
        draw_button(screen, 'red', 220*i - 150, 20, 200,100, 'level '+str(i))

def main(screen):
    global game_over
    global menu_screen
    clock = pygame.time.Clock() # Initialize the clock

    background, bg_image = get_background("Yellow.png")  # Load the background image


    player = Player(100, 100, 50, 50)  # Create a player instance
    tiles()

    offset_x = 0
    scroll_area_width = 400  # Width of the scroll area

    running = True # Main game loop
    while running:
        global event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:  # Check if space key is pressed
                    if player.jump_count < 2:
                        player.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('hi')


        if game_over == False and menu_screen == False:
            player.loop(FPS)  # Update player position
            fire.loop()  # Update fire animation
            handle_move(player, objects) # Handle player movement
            # Fill the screen with the background color
            draw(screen,background,bg_image, player, objects, offset_x)  # Draw the background and player

            if (player.rect.right - offset_x >= SCREEN_WIDTH - scroll_area_width and player.x_vel > 0) or (
                player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0):
                offset_x += player.x_vel
            if player.rect.top > SCREEN_HEIGHT:
                game_over = True
        elif game_over == False and menu_screen == True:
            menu()
        elif game_over == True and menu_screen == False:
            screen.fill('black')
            draw_text('game over', font_big, 'white', 450, 200)
            draw_text('press w to play again', font_big, 'white', 400, 300)
            draw_text('press s to go to menu screen', font_big, 'white', 300, 400)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                game_over = False
                background, bg_image = get_background("Yellow.png")  # Load the background image


                player = Player(100, 100, 50, 50)  # Create a player instance
                tiles()

                offset_x = 0
                scroll_area_width = 400  # Width of the scroll area
            if keys[pygame.K_s]:
                menu_screen = True
                game_over = False
                game_over = False
                background, bg_image = get_background("Yellow.png")  # Load the background image


                player = Player(100, 100, 50, 50)  # Create a player instance
                tiles()

                offset_x = 0
                scroll_area_width = 400  # Width of the scroll area




        # Update the display
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main(screen)

