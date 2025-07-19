import pygame

class SpriteSheet:
  def __init__(self, sheet):
      self.sheet = sheet
  def get_image(sheet, width, height, frame, scale):
      image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()  # Create a new surface with the same size as the sprite
      image.blit(sheet, (0,0), (frame*32,0, width, height))
      width, height = image.get_size()
      image = pygame.transform.scale(image, (width * scale, height * scale))  # Scale the image
      return image
  
class Animation:
  def __init__(self):
    self.frame = 0
    self.animation_steps = 10
    # create animation list
    self.animation_list = []
    self.last_update = pygame.time.get_ticks()
    self.animation_cooldown = 40 # milliseconds


  def load_sprite_sheet(self, directory, screen):
    self.sprite_sheet_image = pygame.image.load(directory).convert_alpha() # Load the sprite sheet image
    self.screen = screen  # Store the screen reference for drawing
    self.direcotory = directory  # Store the directory for debugging
    print(self.direcotory)


    for x in range(self.animation_steps):
      self.animation_list.append(SpriteSheet.get_image(self.sprite_sheet_image, 32, 32, x, 2))  # Get each frame of the sprite sheetz
  def draw_sprite_sheet(self):
    current_time = pygame.time.get_ticks()
    if current_time - self.last_update >= self.animation_cooldown:
      self.last_update = current_time
      self.frame += 1
      if self.frame >= len(self.animation_list):
        self.frame = 0
    self.screen.blit(self.animation_list[self.frame], (self.x, self.y))  # Draw the current frame of the sprite sheet at the specified position
