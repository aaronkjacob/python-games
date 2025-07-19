import pygame

def handle_inputs():
  keys = pygame.key.get_pressed()
  return {
    "a": keys[pygame.K_a],
    "d": keys[pygame.K_d],
    "w": keys[pygame.K_w],
    "s": keys[pygame.K_s],
    "space": keys[pygame.K_SPACE]
  }