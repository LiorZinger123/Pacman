import pygame
from map.create_map import walls

class Walls():

    def __init__(self):
        self.walls = walls

    def print(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 150, 255), wall)