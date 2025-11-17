import pygame
import sys

from constants import *
from graphics.graphics import *
from chess_func import *
from chess_objects import *

def main():
    default = DEFAULT
    game_status, piece_list = fen_to_board_obj(default)
    for i in piece_list:
        print(f'piece:  {i.color} {i.piece} at {i.location}')
    print(vars(game_status))
    fen_string = board_obj_to_fen(piece_list, game_status)
    print(f'Our original string: {default}\nOur new string: {fen_string}')


if __name__ == '__main__':
    main()