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