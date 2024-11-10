import pygame
import random
import math

class GettingOverIt():
    def __init__(self, screen):
        self.screen = screen


    def update(self, screen, held_keys, Gx, Gy, click, Add_Credits):
        screen.fill((0,0,0))
        Add_Credits(1000)

class GettingOverIt2():
    def __init__(self, screen):
        self.screen = screen


    def update(self, screen, held_keys, Gx, Gy, click, Add_Credits):
        screen.fill((0,0,255))
