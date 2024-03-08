import pygame
import time
import sys
from walls.walls import Walls
from coins.coins import Coins
from pacman.pacman import Pacman
from ghosts.ghosts import Ghosts
from cherry.cherry import Cherry

#create screen
pygame.init()
clock = pygame.time.Clock()
width = 456
height = 504
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man")

#updates screen after every frame
def update_screen():
    screen.fill((0, 0, 0))
    w.print(screen)
    c.print(screen)
    g.print(screen)
    p.print(screen)
    cherry.print(screen)
    pygame.display.update()

#start new game
def start_new_game():
    global w, c, p, g, cherry
    w = Walls()
    c = Coins()
    p = Pacman()
    g = Ghosts(p)
    cherry = Cherry()

w, c, p, g, cherry = None, None, None, None, None
start_new_game()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                p.next_direction = "U"
            if event.key == pygame.K_DOWN:
                p.next_direction = "D"
            if event.key == pygame.K_LEFT:
                p.next_direction = "L"
            if event.key == pygame.K_RIGHT:
                p.next_direction = "R"

    p.pacman_functions(w, c, g, cherry)
    g.ghosts_functions()
    cherry.cherry_functions(c, p)
    update_screen()
    clock.tick(125)
    if p.die:
        start_new_game()
    if p.win:
        time.sleep(3)
        break