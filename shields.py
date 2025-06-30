from circleshape import *
from constants import *
import pygame

Class Shield(circleshape):
    def __init__(self, x, y, radius):
        super().__init(x, y, radius)

    def update(self, position, rotation, screen):
        forward = pygame.Vector2(position.x,position.y).rotate(rotation)
        north_west = foward.rotate(-45)
        north_east = forward.rotate(45)
        west = forward.rotate(-90)
        east = forward.rotate(90)
        pygame.draw.line(screen, "white", west, north_west, width=2)
        pygame.draw.line(screen, "white", nort_west, north_east, width=2)
        pygame.draw.line(screen, "white", north_east, east, width=2)
        
    def draw(self):
                
    def collision(self):

