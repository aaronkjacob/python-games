import pygame

def wasd_input():
  keys = pygame.key.get_pressed()
  return {
      'w': keys[pygame.K_w],
      'a': keys[pygame.K_a],
      's': keys[pygame.K_s],
      'd': keys[pygame.K_d]
  }
