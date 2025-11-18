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
    for p in piece_list:
        x, y = p.location
        pos_x = STARTING_X + (x-1)*SQ_SIZE + SQ_SIZE//2
        pos_y = STARTING_Y + (8-y)*SQ_SIZE + SQ_SIZE//2

        filename = f"assets/{p.piece.name}.png"  # e.g., "B.png"
        img = pygame.image.load(filename).convert_alpha()
        img = pygame.transform.smoothscale(img, (int(SQ_SIZE*1.02), int(SQ_SIZE*1.02)))
        rect = img.get_rect(center=(pos_x, pos_y))
        screen.blit(img, rect)

def text_move(game_state, position_list, screen):
    move_string = ''
    error_msg = ''
    running = True
    exit = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state, position_list, error_msg = try_apply_move(move_string, game_state, position_list)
                    place_pieces(screen, position_list)
                    pygame.display.flip()
                    move_string = ''
                    if not error_msg:
                        error_msg = ''
                        running = False
                elif event.key == pygame.K_BACKSPACE:
                    move_string = move_string[:-1]
                else:
                    character = event.unicode
                    if character.isprintable():
                        move_string += character

        screen.fill((0,0,0))
        draw_board(screen)
        place_pieces(screen, position_list)
        move_text = font.render(move_string, True, (WHITE))
        error_text_box = font.render(error_msg, True, (WHITE))
        screen.blit(move_text, (3*SCREEN_WIDTH//4, SCREEN_HEIGHT - 40))
        screen.blit(error_text_box, (2*SCREEN_WIDTH//3, SCREEN_HEIGHT-40-error_text_box.get_height()*3))
        pygame.display.flip()
    return game_state, position_list, exit                

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

        
