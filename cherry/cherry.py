import pygame
import random
import time
import os
from map.create_map import game_board

img_path = os.path.join(os.getcwd(), "cherry\cherry.png")
img = pygame.image.load(img_path)

class Cherry():

    def __init__(self):
        self.x = None
        self.y = None
        self.size = 24
        self.rect = None
        self.image = pygame.transform.scale(img, (self.size, self.size))
        self.positions = []
        self.timer = int(time.time())
        self.count_seconds = 0

    def print(self, screen):
        if self.rect:
            screen.blit(self.image, (self.x, self.y))

    def create_cherry(self, c, p):
        if self.rect == None and self.count_seconds == 10:
            optional_positions = []
            for cube in game_board:
                if cube.y == 216:
                    if cube.x < cube.width * 5 or cube.x > cube.width * 15:
                        continue
                coin_cube = pygame.Rect(cube.x + 9, cube.y + 9, 6, 6)
                big_coin_cube = pygame.Rect(cube.x + 5, cube.y + 5, 14, 14)
                cherry_cube = pygame.Rect(cube.x, cube.y, self.size, self.size)
                if cube != p.cube and coin_cube not in c.coins and big_coin_cube not in c.coins and cherry_cube not in self.positions:
                    optional_positions.append(cube)
            pos = random.choice(optional_positions)
            self.positions.append(pos)
            self.x, self.y = pos.x, pos.y
            self.rect = pygame.Rect(self.x, self.y, self.size ,self.size)

    def count_timer(self):
        if self.count_seconds == 10:
            self.count_seconds = 0
        if int(time.time()) - self.timer == 1:
            self.timer = int(time.time())
            self.count_seconds += 1

    def cherry_functions(self, c, p):
        self.create_cherry(c, p)
        self.count_timer()