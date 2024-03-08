from ghosts.create_ghosts import *

class Ghosts():

    def __init__(self, p):
        self.blinky = Blinky(p)
        self.ghosts = [self.blinky, Pinky(p), Inky(self.blinky, p), Clyde(p)]
        self.pacman = p
        self.start = False

    def print(self, screen):
        for g in self.ghosts:
            g.print(screen, g)

    def start_moving(self):
        for g in self.ghosts:
            if not g.start_moving:
                g.start_move()
    
    def start_game(self):
        for g in self.ghosts:
            if not g.start_game and g.rect == g.home_cubes_rect[0]:
                g.start_game = True
                g.calculate_d = True
                g.same_line = False
    
    def create_escape_targets(self):     
        for g in self.ghosts:
            g.create_escape_targets(g)

    def find_ghosts_targets(self):
        for g in self.ghosts:
            if g.name != "Blinky":
                g.find_target()
    
    def calculate_cubes(self):
        for g in self.ghosts:
            g.calculate_cubes(g, self.pacman)
    
    def move(self):
        for g in self.ghosts:
            if g.start_moving:
                g.move_to_target(g)

    def escape_changes(self):
        for g in self.ghosts:
            g.escape_changes(g)
    
    def escape_mode(self):
        if self.pacman.chase_mode:
            for g in self.ghosts:
                if not g.is_eaten and not g.escape and g not in self.pacman.already_ate:
                   g.enter_escape_mode(g)
        else:
            for g in self.ghosts:
                if g.escape:
                    g.get_out_fron_escaping(g)
        
    def ghosts_functions(self):
        if not self.start:
            self.create_escape_targets()
            self.start = True
        self.start_moving()
        self.find_ghosts_targets()
        self.calculate_cubes()
        self.start_game()
        self.move()
        self.escape_changes()
        self.escape_mode()