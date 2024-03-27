import pygame
import os

size = 24
walls = []
coins = []
game_board = []

map_path = os.path.join(os.getcwd(), "map\map.txt")
map_file = map_path

with open(map_file) as f:
    for y, row in enumerate(f):
        y *= size
        for x, char in enumerate(row):
            x *= size
            if char == '1':
                walls.append(pygame.Rect(x, y, size, size))
            if char == '0':
                coins.append(pygame.Rect(x + 9, y + 9, 6, 6))
                game_board.append(pygame.Rect(x, y, size, size))
            if char == '$':
                coins.append(pygame.Rect(x + 5, y + 5, 14, 14))
                game_board.append(pygame.Rect(x, y, size, size))
            if char == '*':
                game_board.append(pygame.Rect(x, y, size, size))