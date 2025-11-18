import pygame
import sys

from constants import *
from graphics.graphics import *
from example_pgn import *
from data_functions import *
from data_storage import *

def main():
    move_list, fen = pgn_to_move_list(example_pgn)
    print(move_list)
    print(fen)
        

if __name__ == "__main__":
    main()
