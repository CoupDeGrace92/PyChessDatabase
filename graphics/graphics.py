import pygame
import sys
from constants import *
from chess_objects import *
from chess_func import *
from enum import Enum
from data_functions import *

pygame.font.init()
pygame.init()
info_object = pygame.display.Info()
width = info_object.current_w
height = info_object.current_h
sq_width = width//20
sq_height = height//10
size = min(sq_height, sq_width)



font = pygame.font.SysFont(None, 32)

def square_white(row, col):
    sum = row+col
    if sum % 2 == 0:
        return True
    return False

def draw_board(screen, labels=True):
    starting_x = sq_width
    starting_y = sq_height
    sq_size = size
    file_list = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H']
    for i in range(8):
        for j in range(8):
            color = CHESS_GREEN
            if square_white(i,j) == True:
                color = WHITE
            if labels == True and i == 0:
                render_num = str(8-j)
                text_surface = font.render(render_num,True, WHITE)
                screen.blit(text_surface, (starting_x - sq_size/2, starting_y + j*sq_size + sq_size//2 - text_surface.get_height()//2))
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
    for p in piece_list:
        x, y = p.location
        pos_x = sq_width + (x-1)*size + size//2
        pos_y = sq_height + (8-y)*size + size//2

        filename = f"assets/{p.piece.name}.png"  # e.g., "B.png"
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.smoothscale(img, (int(size*1.02), int(size*1.02)))
        rect = img.get_rect(center=(pos_x, pos_y))
        screen.blit(img, rect)        

def try_apply_move(move_string, game_state, position_list):
    try:
        source, destination, castling, ep, capture, promotion = algebraic_to_move(move_string, game_state, position_list)
        if source is None or destination is None:
            raise ValueError("Illegal move: no source/destination OR improperly formatted move: ")
        new_gamestate, new_position = move(game_state, position_list, source, destination, castling, ep, capture, promotion)
        if new_gamestate is None or new_position is None:
            raise ValueError("Illegal move: move() failed:  ")
        return new_gamestate, new_position, None
    except KeyError as e:
        bad_key = e.args[0]
        return game_state, position_list, f'Bad key in the piece list: {bad_key}.  Attempted move: {move_string}'
    except Exception as e:
        error_msg = str(e)+f'{move_string}'
        return game_state, position_list, error_msg

        
def text_move_tree(position_node, screen):
    game_state, position_list = fen_to_board_obj(position_node.fen)
    move_string = ''
    error_msg = ''
    running = True
    exit = False
    current_node = position_node
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state, position_list, error_msg = try_apply_move(move_string, game_state, position_list)
                    current_node = algebraic_to_new_node(move_string, position_node)
                    place_pieces(screen, position_list)
                    pygame.display.flip()
                    move_string = ''
                    if not error_msg:
                        error_msg = ''
                        running = False
                elif event.key == pygame.K_BACKSPACE:
                    move_string = move_string[:-1]
                elif event.key == pygame.K_LEFT:
                    if position_node.parents:
                        current_node = position_node.parents
                        game_state, position_list = fen_to_board_obj(current_node.fen)
                        running = False
                elif event.key == pygame.K_RIGHT:
                    if position_node.children:
                        if len(position_node.children)==1:
                            for child in position_node.children:
                                current_node = position_node.children[child]
                                game_state, position_list = fen_to_board_obj(current_node.fen)
                                running = False
                else:
                    character = event.unicode
                    if character.isprintable():
                        move_string += character

        screen.fill((0,0,0))
        draw_board(screen)
        place_pieces(screen, position_list)

        draw_move_color_square(screen, current_node)

        move_text = font.render(move_string, True, (WHITE))
        error_text_box = font.render(error_msg, True, (WHITE))
        screen.blit(move_text, (3*width//4, height - 2*size))
        screen.blit(error_text_box, (2*width//3, height-2*size-error_text_box.get_height()*3))
        pygame.display.flip()
    return current_node, exit

def draw_move_color_square(screen, position_node):
    fen = position_node.fen
    game_state, position_list = fen_to_board_obj(fen)
    player_turn = game_state.player_turn
    color = WHITE
    turn_sq_size = size//3
    inner_size = turn_sq_size//8
    if player_turn == 'white':
        pygame.draw.rect(screen, color, (int(sq_width * 9.5), sq_height, turn_sq_size, turn_sq_size))
    else:
        pygame.draw.rect(screen, color, (int(sq_width*9.5), sq_height, turn_sq_size, turn_sq_size), inner_size)

def display_moves(screen, move_list):
    NotImplemented

def display_candidates(screen, position_node):
    NotImplemented