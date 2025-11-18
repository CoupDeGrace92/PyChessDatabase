import pygame
import sys

from constants import *
from graphics.graphics import *
from data_functions import *
from data_storage import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 32)

def main():
    print("Initializing Chess Board")
    print(f"Screen width:{SCREEN_WIDTH}")
    print(f"Screen height:{SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game_data, position_list = fen_to_board_obj(DEFAULT)
    exit = False

    while True:
        if exit == True:
            return

        game_data, position_list, exit = text_move(game_data, position_list, screen)
        

if __name__ == "__main__":
    main()
