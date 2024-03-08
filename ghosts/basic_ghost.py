import pygame
import time
from map.create_map import game_board

opposite_directions = {"U": "D", "D": "U", "L": "R", "R": "L"}
width = 456

class BasicGhost():

    def __init__(self):
        self.size = 24
        self.original_speed = 0.75
        self.speed = self.original_speed
        self.escape_speed = 0.5
        self.back_home_speed = 2
        self.direction = ""
        self.next_cube = None
        self.same_line = False
        self.future_d = None
        self.cube = None
        self.t_cube = None
        self.start_game = False
        self.escape = False
        self.distance_x = None
        self.distance_y = None
        self.change_d = False
        self.is_eaten = False
        self.change_d_now = False
        self.first_come_back = False
        self.ghost_escape_color_1 = (0, 0, 255)
        self.ghost_escape_color_2 = (190, 210, 170)
        self.back_home_timer = 0
        self.back_home_counter = 0

    def print(self, screen, rect): #print ghost
        pygame.draw.ellipse(screen, self.color, rect)
    
    def create_escape_targets(self, g): #create ghosts escaping targets
        g.escape_targets = []
        for t_x, t_y in g.escape_targets_coordinations:
            g.escape_targets.append(pygame.Rect(t_x, t_y, self.size, self.size))
    
    def calculate_cube(self, g, x, y, if_target): #calculate the cube that the player/ghost
        player_cube, player_min_distance_x, player_min_distance_y = None, self.size, self.size
        for cube in game_board:
            if abs(x - cube.x) < self.size and abs(y - cube.y) < self.size:
                if abs(x - cube.x) < player_min_distance_x and abs(y - cube.y) < player_min_distance_y:
                    player_cube = cube
                    player_min_distance_x = abs(x - cube.x)
                    player_min_distance_y = abs(y - cube.y)
        if not player_cube:
            if not g.start_game or (g.is_eaten and g.first_come_back):
                return pygame.Rect(x, y, self.size, self.size)
            elif if_target and g.name != "Blinky":
                return self.calculate_New_T_Cube(g.target, g.basic_target.direction)
        return player_cube
    
    def calculate_New_T_Cube(self, rect, d): #calculate target cube if pacman is near walls
        checking_rect = rect
        checking_rect = self.move_ghost(opposite_directions[d], checking_rect.x, checking_rect.y)
        if checking_rect in game_board:
            return checking_rect
        else:
            checking_rect = self.move_ghost(opposite_directions[d], checking_rect.x, checking_rect.y)
            for direction in opposite_directions.keys():
                if direction != d and direction != opposite_directions[d]:
                    check_move = self.move_ghost(direction, checking_rect.x, checking_rect.y)
                    if check_move in game_board:
                        return check_move
            return checking_rect

    def calculate_cubes(self, g, p): #calculate both cubes
        g.cube = g.calculate_cube(g, g.x, g.y, False)
        if g.escape and g.start_game:
            if not g.is_eaten:
                if g.cube == g.t_cube:
                    g.escape_targets.append(g.escape_targets.pop(0))
                g.t_cube = g.escape_targets[0]
        elif not g.escape and g.is_eaten:
            if g.cube == g.t_cube:
                if not g.first_come_back:
                    g.first_come_back = True
                    g.t_cube = g.home_cubes_rect[1]
                else:
                    self.get_out_fron_escaping(g)
                    g.t_cube = g.home_cubes_rect[0]
        else:
            g.t_cube = g.calculate_cube(g, g.target.x, g.target.y, True)
    
    def enter_escape_mode(self, g):
        g.escape = True
        g.color = g.ghost_escape_color_1
        g.change_d_now = True
    
    def escape_changes(self, g): #changes ghost speed and color in escape mode
        if not g.escape:
            if not g.is_eaten and g.speed == g.escape_speed:
                if (isinstance(g.x, int) or str(g.x)[-1] == '0') and (isinstance(g.y, int) or str(g.y)[-1] == '0'):
                    if g.x % g.original_speed == 0 and g.y % g.original_speed == 0:
                        g.speed = g.original_speed
            if g.is_eaten:
                if g.speed == g.escape_speed:
                    if (isinstance(g.x, int) or str(g.x)[-1] == '0') and (isinstance(g.y, int) or str(g.y)[-1] == '0'):
                        if g.x % g.back_home_speed == 0 and g.y % g.back_home_speed == 0:
                            g.speed = g.back_home_speed
                if time.time() - self.back_home_timer >= 0.1:
                    self.back_home_timer = time.time()
                    self.back_home_counter += 1
                    if self.back_home_counter % 2 == 1:
                        self.color = self.ghost_escape_color_2
                    else:
                        self.color = self.ghost_escape_color_1
        else:
            if g.speed == g.original_speed:
                if (isinstance(g.x, int) or str(g.x)[-1] == '0' or str(g.x)[-2] == '.5') and (isinstance(g.y, int) or str(g.y)[-1] == '0' or str(g.y)[-2] == '.5'):
                    g.speed = g.escape_speed
        
    def enter_eaten_mode(self, g):
        g.escape = False
        g.is_eaten = True
        g.t_cube = g.home_cubes_rect[0]
        g.back_home_timer = time.time()
        g.back_home_counter = 0
        g.change_d_now = True
    
    def get_out_fron_escaping(self, g): #get out from escape mode
        g.color = g.original_color
        g.back_home_timer = 0
        g.back_home_counter = 0
        if not g.is_eaten:
            g.escape = False
        else:
            g.is_eaten = False
            g.start_game = False
            g.first_come_back = False
            g.calculate_d = False
            g.future_d = []
            g.speed = g.original_speed
    
    def move_ghost(self, d, x, y): #checks future movement of the ghost
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
            
    def check_future_of_next_move(self, d1, d2, rect): #makes ghosts move efficiently
        count = 0
        checking_rect = rect
        while True:
            checking_rect = self.move_ghost(d1, checking_rect.x, checking_rect.y)
            if checking_rect in game_board:
                count += 1
                rect2 = self.move_ghost(d2, checking_rect.x, checking_rect.y)
                if rect2 in game_board:
                    return count
                checking_rect = rect2
            else:
                return 0
    
    def same_line_with_target(self, d, rect, current_d): #deals with situations when ghost and target are in the same line
        count1 = self.check_future_of_next_move(d[1], d[0], rect)
        count2 = self.check_future_of_next_move(d[2], d[0], rect)
        if count1 < count2 and count1 != 0:
            return d[1]
        elif count2 < count1 and count2 != 0:
            return d[2]
        elif count1 == count2:
            if current_d == d[1]:
                return d[1]
            return d[2]
        elif count1 == 0:
            return d[2]
        else:
            return d[1]
    
    def efficient_move(self, g, d, i): #makes ghost move efficiently in close turn situations
        count = 0
        checking_rect = g.rect
        check_current_turn = self.move_ghost(d[1], checking_rect.x, checking_rect.y)
        behind_rect = self.move_ghost(opposite_directions[d[0]], checking_rect.x, checking_rect.y)
        behind_turn = self.move_ghost(d[1], behind_rect.x, behind_rect.y)
        if check_current_turn not in game_board and behind_turn not in game_board:
            return False
        while True:
            next_move = self.move_ghost(d[0], checking_rect.x, checking_rect.y)
            if next_move in game_board:
                checking_rect = next_move
                count += 1
            else:
                break
        if count > 0 and (count < 3 or count > 6):
            if i == 0 and count > 6 and check_current_turn in game_board:
                if self.check_future_of_next_move(d[0], d[1], g.cube) < count:
                    return False
                return True
            check_end_turn = self.move_ghost(d[1], checking_rect.x, checking_rect.y)
            if check_end_turn in game_board:
                return False
            else:
                if check_current_turn not in game_board and behind_turn in game_board:
                    g.future_d.pop(1)
                return True
        return False
    
    def change_d_when_changing_target(self, g, distance_x, distance_y):
        if (distance_x < self.size * 4 or distance_y < self.size * 4) and g.start_game:
            if self.move_ghost(g.future_d[0], g.cube.x, g.cube.y) not in game_board:
                count1 = self.check_future_of_next_move(g.future_d[1], g.future_d[0], g.cube)
                count2 = self.check_future_of_next_move(opposite_directions[g.future_d[1]], g.future_d[0], g.cube)
                if count1 != 0 or count2 != 0:
                    if count1 == count2 and count1 != 0:
                        d = self.same_line_with_target(g.future_d, g.cube, g.direction)
                        g.future_d = [g.future_d[0], d]
                        g.direction = g.future_d[1]
                    if count1 != 0:
                        if count2 == 0 or (count2 != 0 and count1 < count2):
                            g.direction = g.future_d[1]
                            g.future_d.pop()
                    elif count2 != 0:
                        if count1 == 0 or (count1 != 0 and count2 < count1):
                            g.direction = opposite_directions[g.future_d[1]]
                            g.future_d.pop(1)
                    g.calculate_d = False
                    return True
        if g.future_d[0] == opposite_directions[g.direction] or g.future_d[1] == opposite_directions[g.direction]:
            if g.future_d[0] == opposite_directions[g.direction]:
                new_g = self.move_ghost(g.future_d[0], g.x, g.y)
                if self.calculate_cube(g, new_g.x, new_g.y, False) in game_board:
                    g.direction = g.future_d[0]
            else:
                new_g = self.move_ghost(g.future_d[1], g.x, g.y)
                if self.calculate_cube(g, new_g.x, new_g.y, False) in game_board:
                    g.direction = g.future_d[1]

    def will_out_of_bounds(self, g, d):
        if g.y == 216:
            if (g.x == g.size * 4 and d == "L") or (g.x == width - g.size * 5 and d == "R"):
                if g.y > g.target.y:
                    g.direction = "U"
                else:
                    g.direction = "D"
                return True
    
    def home_situations(self, g): #when ghost needs to enter home or exit home
        if (g.x >= self.size * 8 and g.x <= self.size * 10 and g.y >= self.size * 8 and g.y <= self.size * 10) and not g.first_come_back:
            g.direction = "U"
            return True
        if g.first_come_back:
            g.direction = "D"
            return True
        return False
    
    def g_reach_original_target(self, g):
        g.reach_original_target = True
        g.last_pacman_position = pygame.Rect(g.basic_target.x, g.basic_target.y, g.size, g.size)
        g.t_cube = g.calculate_cube(g, g.basic_target.x, g.basic_target.y, True)
        g.back_to_original_target = int(time.time())
        g.count_time_until_original_target = 3
    
    def back_to_original(g):
        if g.count_time_until_original_target == 0:
            g.reach_original_target = False
            g.back_to_original_target = 0
            g.count_time_until_original_target = 3
        if int(time.time()) - g.back_to_original_target == 1:
            g.back_to_original_target = int(time.time())
            g.count_time_until_original_target -= 1

    def move_to_target(self, g): #eventually chooses ghost direction
        if g.cube == None:
            print(g.name, g.future_d, g.calculate_d, g.same_line)
            time.sleep(20)
        if (g.x == g.cube.x and g.y == g.cube.y) or g.change_d_now:
            
            if g.name != "Blinky":
                if g.cube == g.t_cube:
                    if not g.reach_original_target:
                        g.g_reach_original_target(g)
                else:
                    if g.reach_original_target:
                        g.back_to_original()
            
            if g.cube.x == g.t_cube.x or g.cube.y == g.t_cube.y:
                g.same_line = True

            if not g.same_line and (g.distance_x == -(g.cube.x - g.t_cube.x) or g.distance_y == -(g.cube.y - g.t_cube.y)):
                g.same_line = True
                
            g.distance_x = g.cube.x - g.t_cube.x
            g.distance_y = g.cube.y - g.t_cube.y
            distance_x = abs(g.distance_x)
            distance_y = abs(g.distance_y)
            next_cube_rect = pygame.Rect(0, 0, 25, 25)
            
            if g.calculate_d or g.change_d_now:
                g.future_d = []
                g.future_d.append("R") if g.cube.x < g.t_cube.x else g.future_d.append("L")
                g.future_d.append("D") if g.cube.y < g.t_cube.y else g.future_d.append("U")
                if distance_y > distance_x or (distance_x == distance_y and (g.direction == "U" or g.direction == "D")):
                    g.future_d.reverse()
                g.future_d.append(opposite_directions[g.future_d[1]])
           
            if not self.home_situations(g):
                for i in range(len(g.future_d)):
                    d = g.future_d[i]
                    if g.change_d_now:
                        self.change_d_when_changing_target(g, distance_x, distance_y)
                        g.change_d_now = False
                        break                        
                    if not g.calculate_d and len(g.future_d) == 2:
                        if self.move_ghost(g.future_d[0], g.x, g.y) not in game_board and self.move_ghost(g.future_d[1], g.x, g.y) not in game_board:
                            g.direction = opposite_directions[g.future_d[1]]
                            g.calculate_d = True
                    if g.calculate_d and not g.first_come_back and not g.same_line and self.efficient_move(g, g.future_d, i):
                        g.direction = g.future_d[len(g.future_d) - 2]
                        if len(g.future_d) == 3:
                            g.future_d.pop()
                        break
                    if (g.same_line and i == 1 and not g.change_d and len(g.future_d) == 3) or i == 2:
                        if i == 2:
                            g.future_d.pop(1)
                        else:
                            d = self.same_line_with_target(g.future_d, g.cube, g.direction)
                            g.future_d = [g.future_d[0], d]
                            g.change_d = True
                        g.calculate_d = False
                        g.direction = d
                        break
                    next_cube_rect = self.move_ghost(d, g.cube.x, g.cube.y)
                    if next_cube_rect in game_board:
                        if not g.calculate_d and i == 0:
                            g.calculate_d = True
                            g.efficient_movement = False
                        if g.same_line:
                            g.same_line = False
                            g.change_d = False
                        g.direction = d
                        break
        self.move(g)
    
    def move(self, g): #actualy move the ghost
        self.will_out_of_bounds(g, g.direction)
        match g.direction:
            case "U":
                g.y -= g.speed
            case "D":
                g.y += g.speed
            case "L":
                g.x -= g.speed
            case "R":
                g.x += g.speed
        g.rect = pygame.Rect(g.x, g.y, g.size, g.size)