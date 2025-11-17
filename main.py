import pygame
import sys

from constants import *
from graphics.graphics import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 32)

def main():
    print("Initializing Chess Board")
    print(f"Screen width:{SCREEN_WIDTH}")
    print(f"Screen height:{SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        screen.fill((0,0,0))
        draw_board(screen)

        starting_game_data, starting_piece_list = fen_to_board_obj(TEST_FEN)
        place_pieces(screen, starting_piece_list)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
