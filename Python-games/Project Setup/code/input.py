import pygame
from pygame.locals import *

# Checks for user input and returns the corresponding action

def handle_input():    
  keys = pygame.key.get_pressed()    
  if keys[K_LEFT]:
    return "LEFT"   
  elif keys[K_RIGHT]:       
    return "RIGHT"    
  elif keys[K_UP]:        
    return "UP"    
  elif keys[K_DOWN]:      
    return "DOWN"    
  elif keys[K_SPACE]:     
    return "JUMP"    
  elif keys[K_ESCAPE]:    
    return "QUIT"    
  else:                   
    return None