import pygame
from InheritClass import Inherit

class Player(Inherit):
    def __init__(self, x, y, img):
        super().__init__(x, y)
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.right = False
        self.left = False
        self.momentum = 0
        self.air_timer = 0
        self.flip = False
        self.action = 'idle'
        self.frame = 0
        self.flip = False