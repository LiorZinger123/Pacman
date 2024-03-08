import pygame
import math
from ghosts.basic_ghost import BasicGhost

width = 456
height = 504

class Blinky(BasicGhost):

    def __init__(self, target):
        super().__init__()
        self.name = "Blinky"
        self.x = 216
        self.y = 168
        self.original_color = (255, 0, 0)
        self.color = self.original_color
        self.calculate_d = True
        self.start_moving = True
        self.home_cubes_rect = [pygame.Rect(216, 168, self.size, self.size), pygame.Rect(216, 216, self.size, self.size)]
        self.target = target
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.escape_targets_coordinations = [(width - self.size * 5, self.size * 3), (width - self.size * 5, self.size), (width - self.size * 2, self.size), (width - self.size * 2, self.size * 3)]
        self.escape_targets = None

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

class Pinky(BasicGhost):

    def __init__(self, target):
        super().__init__()
        self.name = "Pinky"
        self.x = 216
        self.y = 216
        self.home_cubes_rect = [pygame.Rect(216, 168, self.size, self.size), pygame.Rect(216, 216, self.size, self.size)]
        self.original_color = (255,192,203)
        self.calculate_d = False
        self.start_moving = True
        self.color = self.original_color
        self.basic_target = target
        self.target = self.home_cubes_rect[0]
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.escape_targets_coordinations = [(self.size * 4, self.size * 3), (self.size * 4, self.size), (self.size, self.size), (self.size, self.size * 3)]
        self.escape_targets = None
        self.reach_original_target = False
        self.back_to_original_target = None
        self.count_time_until_original_target = None

    def find_target(self): #finds ghost target
        if self.start_game and not self.escape and not self.is_eaten:
            self.target = pygame.Rect(self.basic_target.x, self.basic_target.y, self.size, self.size)
            if not self.reach_original_target:
                match self.basic_target.direction:
                    case "U":
                        self.target.y -= self.size * 2
                    case "D":
                        self.target.y += self.size * 2
                    case "L":
                        self.target.x -= self.size * 2
                    case "R":
                        self.target.x += self.size * 2

class Inky(BasicGhost):

    def __init__(self, blinky, target):
        super().__init__()
        self.name = "Inky"
        self.blinky = blinky
        self.x = 192 
        self.y = 216
        self.home_cubes_rect = [pygame.Rect(192, 168, self.size, self.size), pygame.Rect(192, 216, self.size, self.size)]
        self.original_color = (125, 249, 255)
        self.calculate_d = False
        self.start_moving = False
        self.color = self.original_color
        self.basic_target = target
        self.target = self.home_cubes_rect[0]
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.escape_targets_coordinations = [(width - self.size * 7, height - self.size * 6), (width - self.size * 5, height - self.size * 6),
        (width - self.size * 5, height - self.size * 4), (width - self.size * 2, height - self.size * 4),
        (width - self.size * 2, height - self.size * 2), (width - self.size * 9, height - self.size * 2),
        (width - self.size * 9, height - self.size * 4), (width - self.size * 7, height - self.size * 4)]
        self.escape_targets = None
        self.reach_original_target = False
        self.back_to_original_target = None
        self.count_time_until_original_target = None

    def find_target(self): #finds ghost target
        if self.start_game and not self.escape and not self.is_eaten:
            self.target = pygame.Rect(self.basic_target.x, self.basic_target.y, self.size, self.size)
            if not self.reach_original_target:
                match self.basic_target.direction:
                    case "U":
                        self.target.y -= self.size
                    case "D":
                        self.target.y += self.size
                    case "L":
                        self.target.x -= self.size
                    case "R":
                        self.target.x += self.size
                blinky_x = self.blinky.get_x()
                blinky_y = self.blinky.get_y()
                d_x = abs(self.target.x - blinky_x)
                d_y = abs(self.target.y - blinky_y)
                if blinky_x < self.target.x:
                    self.target.x += d_x
                else:
                    self.target.x -= d_x
                if blinky_y < self.target.y:
                    self.target.y += d_y
                else:
                    self.target.y -= d_y
                self.out_bound_target()

    def out_bound_target(self):
        while (self.target.x > 0 and self.target.x < self.size * 4) and (self.target.y > self.size * 6 and self.target.y < self.size * 14):
            self.target.x += self.size
        while (self.target.x < width and self.target.x > width - self.size * 4) and (self.target.y > self.size * 6 and self.target.y < self.size * 14):
            self.target.x -= self.size
        while self.target.x <= self.size:
            self.target.x += self.size
        while self.target.x >= width - self.size:
            self.target.x -= self.size
        while self.target.y <= self.size:
            self.target.y += self.size
        while self.target.y >= height - self.size:
            self.target.y -= self.size

    def start_move(self):
        if not self.start_moving and self.basic_target.eaten_dots == 30:
            self.start_moving = True

class Clyde(BasicGhost):

    def __init__(self, target):
        super().__init__()
        self.name = "Clyde"
        self.x = 240
        self.y = 216
        self.home_cubes_rect = [pygame.Rect(240, 168, self.size, self.size), pygame.Rect(240, 216, self.size, self.size)]
        self.original_color = (255, 165, 0)
        self.calculate_d = False
        self.start_moving = False
        self.color = self.original_color
        self.basic_target = target
        self.target = self.home_cubes_rect[0]
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.escape_targets_coordinations = [(self.size * 6, height - self.size * 6), (self.size * 4, height - self.size * 6),
        (self.size * 4, height - self.size * 4), (self.size, height - self.size * 4),
        (self.size, height - self.size * 2), (self.size * 8, height - self.size * 2),
        (self.size * 8, height - self.size * 4), (self.size * 6, height - self.size * 4)]
        self.escape_targets = None
        self.reach_original_target = False
        self.back_to_original_target = None
        self.count_time_until_original_target = None
        self.target_index = 0

    def find_target(self): #finds ghost target
        if self.start_game and not self.escape and not self.is_eaten:
            self.target = pygame.Rect(self.basic_target.x, self.basic_target.y, self.size, self.size)
            if math.dist([self.x, self.y], [self.target.x, self.target.y]) < self.size * 10:
                self.change_close_target()
                self.target = self.escape_targets[self.target_index]            
    
    def change_close_target(self):
        if abs(self.x - self.escape_targets[self.target_index].x) < 1 and abs(self.y - self.escape_targets[self.target_index].y) < 1:
            self.target_index += 1
            if self.target_index == len(self.escape_targets):
                self.target_index = 0
    
    def start_move(self):
        if not self.start_moving and self.basic_target.eaten_dots == 62:
            self.start_moving = True