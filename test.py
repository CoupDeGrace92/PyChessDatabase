import pygame
import sys

from constants import *
from graphics.graphics import *
from data_functions import *
from data_storage import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 32)

info_object = pygame.display.Info()
screen_width = info_object.current_w
screen_height = info_object.current_h

def main():
    print("Initializing Chess Board")
    print(f"Screen width:{screen_width}")
    print(f"Screen height:{screen_height}")

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    exit = False
    current_node = PositionNode(DEFAULT)

    while True:
        if exit == True:
            return


        current_node, exit = text_move_tree(current_node, screen)

        

if __name__ == "__main__":
    main()
