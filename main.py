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

    exit = False
    current_node = PositionNode(DEFAULT)

    while True:
        if exit == True:
            return


        current_node, exit = text_move_tree(current_node, screen)
        

if __name__ == "__main__":
    main()
