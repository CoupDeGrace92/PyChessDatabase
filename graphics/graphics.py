import pygame
import sys
from constants import *
from chess_objects import *
from chess_func import *
from enum import Enum

pygame.font.init()

font = pygame.font.SysFont(None, 32)

def square_white(row, col):
    sum = row+col
    if sum % 2 == 0:
        return True
    return False

def draw_board(screen, labels=True):
    starting_x = STARTING_X
    starting_y = STARTING_Y
    sq_size = SQ_SIZE
    file_list = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H']
    for i in range(8):
        for j in range(8):
            color = CHESS_GREEN
            if square_white(i,j) == True:
                color = WHITE
            if labels == True and i == 0:
                render_num = str(8-j)
                text_surface = font.render(render_num,True, WHITE)
                screen.blit(text_surface, (starting_x - 50, starting_y*j+sq_size*3/2 - text_surface.get_height()//2))
            pygame.draw.rect(screen, color, (starting_x+sq_size*i,starting_y+sq_size*j,sq_size,sq_size))
    if labels:
        file_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        bottom_y_coord = starting_y+8*sq_size
        for i, letter in enumerate(file_list):
            text = font.render(letter, True, WHITE)
            tx = starting_x + i * sq_size + sq_size//2 - text.get_width()//2
            ty = bottom_y_coord + sq_size//5
            screen.blit(text, (tx,ty))

def place_pieces(screen, piece_list):
    for i in piece_list:
        location = i.location
        pos_x = STARTING_X + (location[0]-1)*SQ_SIZE + SQ_SIZE//2
        pos_y = STARTING_Y + (8-location[1])*SQ_SIZE + SQ_SIZE//2
        piece = PieceType(i.color + ' ' + i.piece)
        piece_name = piece.name
        image_filepath = 'assets/'+piece_name+'.png'
        image_with_alpha = pygame.image.load(image_filepath).convert_alpha()
        image_scaled = pygame.transform.smoothscale(image_with_alpha, (SQ_SIZE*1.02, SQ_SIZE*1.02))
        image_rect = image_scaled.get_rect(center = (pos_x, pos_y))
        screen.blit(image_scaled, image_rect)
