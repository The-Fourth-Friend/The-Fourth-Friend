import pygame
from InheritClass import Inherit
class Player(Inherit):
    def __init__(self, x, y):
        super().__init__(x, y)
        #self.img = img
        #self.mask = pygame.mask.from_surface(self.img)
        self.right = False
        self.left = False
        self.momentum = 0
        self.air_timer = 0
        self.facing_left = False
        self.walk_count = 0
        self.idle = True
        self.run_count = 0