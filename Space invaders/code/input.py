import pygame

def keyPressed():
  keys = pygame.key.get_pressed()
  if keys[pygame.K_a]:
    return 'a'
  if keys[pygame.K_d]:
    return 'd' 
  if keys[pygame.K_SPACE]:
    return 'space'