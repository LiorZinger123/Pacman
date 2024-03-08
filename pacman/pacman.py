import pygame
import time
from map.create_map import game_board

width = 456

class Pacman:

    def __init__(self):
        self.size = 24
        self.x = 216
        self.y = 360
        self.speed = 1
        self.direction = "L"
        self.next_direction = ""
        self.eaten_dots = 0
        self.score = 0
        self.chase_mode = False
        self.chase_timer = 0
        self.chase_count_down = None
        self.took_another_big_coin = False
        self.rect = None
        self.die = False
        self.win = False
        self.already_ate = []
        self.cube = None

    def print(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 0), self.rect)

    def move(self):
        if self.x > width - self.size and self.direction == "R":
            self.x = 0
        elif self.x < 0 and self.direction == "L":
            self.x = width - self.size
        else:
            match self.direction:
                case "U":
                    self.y -= self.speed
                case "D":
                    self.y += self.speed
                case "L":
                    self.x -= self.speed
                case "R":
                    self.x += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def change_direction(self, w):
        if not self.direction or (self.next_direction and self.next_direction != self.direction): # If not moving or changing direction
            if not self.check_next_move(self.next_direction, w) and (self.x > -self.size and self.x < 475): # can move and stay inside the game
                self.direction = self.next_direction
                self.next_direction = ""
    
    def check_next_move(self, d, items):
        x, y = self.x, self.y
        match d:
            case "U":
                y -= self.speed
            case "D":
                y += self.speed
            case "L":
                x -= self.speed
            case "R":
                x += self.speed
        player_rect = pygame.Rect(x, y, self.size, self.size)
        for item in items:
            if player_rect.colliderect(item):
                return True
        return False
    
    def move_pacman(self, w):
        if not self.check_next_move(self.direction, w):
            self.move()
    
    def check_if_eat_a_coin(self, c, rect):
        for coin in c.coins:
            if rect.colliderect(coin):
                return coin
        return None
    
    def eat_coin(self, c, g):
        coin = self.check_if_eat_a_coin(c, self.rect)
        if coin:
            c.remove_coin(coin)
            self.eaten_dots += 1
            if coin.width == 14:
                g.create_escape_targets()
                if self.chase_mode:
                    self.took_another_big_coin = True
                self.chase_mode = True
                self.chase_count_down = 10
                self.already_ate = []
                self.chase_timer = int(time.time())
                self.score += 10
            else:
                self.score += 5
            return True

    def count_down(self, g):
        if self.chase_mode:
            if self.chase_count_down == 0:
                self.chase_mode = False
                self.chase_count_down = 10
                self.took_another_big_coin = False
                self.alreay_ate = []
            elif int(time.time()) - self.chase_timer == 1:
                self.chase_timer = int(time.time())
                self.chase_count_down -= 1

    def eat_or_die(self, ghosts):
        for g in ghosts.ghosts:
            if self.rect.colliderect(g.rect):
                if g.escape and g not in self.already_ate:
                    g.enter_eaten_mode(g)
                    self.already_ate.append(g)
                    self.score += 200
                elif not g.escape and not g.is_eaten:
                    self.die = True
    
    def eat_cherry(self, cherry):
        if cherry.rect and self.rect.colliderect(cherry.rect):
            self.score += 100
            cherry.rect = None
            cherry.count_seconds = 0

    def check_if_win(self, c):
        if not c.coins:
            self.win = True

    def calculate_pacmans_cube(self):
        player_cube, player_min_distance_x, player_min_distance_y = None, self.size, self.size
        for cube in game_board:
            if abs(self.x - cube.x) < self.size and abs(self.y - cube.y) < self.size:
                if abs(self.x - cube.x) < player_min_distance_x and abs(self.y - cube.y) < player_min_distance_y:
                    player_cube = cube
                    player_min_distance_x = abs(self.x - cube.x)
                    player_min_distance_y = abs(self.y - cube.y)
        self.cube = player_cube
    
    def calculate_pacmans_next_cube(self, d):
        x, y = self.cube.x, self.cube.y
        match d:
            case "U":
                y -= self.size
            case "D":
                y += self.size
            case "L":
                x -= self.size
            case "R":
                x += self.size
        return pygame.Rect(x, y, self.size, self.size)
                
    def pacman_functions(self, w, c, g, cherry):
        self.calculate_pacmans_cube()
        self.change_direction(w.walls)
        self.move_pacman(w.walls)
        self.eat_coin(c, g)
        self.count_down(g)
        self.eat_or_die(g)
        self.eat_cherry(cherry)
        self.check_if_win(c)