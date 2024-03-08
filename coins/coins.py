import pygame
from map.create_map import coins

class Coins:

    def __init__(self):
        self.coins = coins
            
    def print(self, screen):
        for coin in self.coins:
            pygame.draw.ellipse(screen, (255, 255, 255), coin)
    
    def remove_coin(self, eaten_coin):
        self.coins = list(filter(lambda coin: coin != eaten_coin, self.coins))