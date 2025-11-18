from constants import *
import re
from data_storage import *
from chess_func import *
from chess_objects import *

def pgn_to_move_list(pgn):
    move_list = []
    fen_obj = re.search(r'\[FEN\s+"([^"]*)"\]', pgn)
    if fen_obj:
        fen = fen_obj.group(1) 
    else:
        fen = DEFAULT
    pgn_lines = pgn.split('\n')
    for i in range(len(pgn_lines)):
        line = pgn_lines[i].strip()
        if line == '':
             continue
        elif not (line.startswith('[') and line.endswith(']')):
            move_pgn = ' '.join(pgn_lines[i:])
            break
    active_game = True
    current_string = ''
    while active_game == True:

        current_char = move_pgn[0]
        if current_char.isnumeric():
            if current_char == 0:
                kingside = ''.join(move_pgn[0:3])
                queenside = ''.join(move_pgn[0:5])
                if queenside == '0-0-0':
                    move_list.append(queenside)
                    move_pgn = move_pgn[4:]
                elif kingside == '0-0':
                    move_list.append(kingside)
                    move_pgn = move_pgn[2:]
                else:
                    current_string = ''
            elif current_string:
                current_string += current_char
            else:
                current_string = ''
        elif current_char.isalpha():
            if current_char == 'O':
                kingside = ''.join(move_pgn[0:3])
                queenside = ''.join(move_pgn[0:5])
                if queenside == 'O-O-O':
                    move_list.append('0-0-0')
                    move_pgn = move_pgn[4:]
                elif kingside == 'O-O':
                    move_list.append('0-0')
                    move_pgn = move_pgn[2:]
                else:
                    current_string = ''
            else:
                current_string += current_char
        elif current_char == ' ':
            if current_string:
                move_list.append(current_string)
                current_string = ''
        elif current_char == '{':
            move_pgn=re.sub(r'{[\s\S]*?}',' ',move_pgn)  #We can adjust this to a capture group with () to save a comment, probably just save as a comment object to avoid regexing in the future
            current_string = ''
        elif current_char == '=':
            current_string += current_char

        #If we wanted to keep variations - elif current_char == '(', save it to the list as the next char

        if len(move_pgn) > 1:
            move_pgn = move_pgn[1:] #This is for length greater than 1
        else:
            move_pgn = ''
            active_game = False

    return move_list, fen

def generate_base_move_tree(pgn_list, fen):
    root_node = PositionNode(fen)
    root_node.count_games +=1
    root_node.children = {}

    fen_list = []
    current_fen = fen
    for move in pgn_list:
        game_state, piece_list = fen_to_board_obj(current_fen)
        source, destination, castling, ep, capture, promotion = algebraic_to_move(move, game_state, piece_list)
        game_state, piece_list = move(game_state, piece_list, source, destination, castling, ep, capture, promotion)
        current_fen = board_obj_to_fen(piece_list, game_state)
        fen_list.append(current_fen)
    node = root_node
    for fen in fen_list:   
        if node.children is None:
            node.children = {}

        child = node.children.get(fen)
        if child is None:
            child = PositionNode(fen)
            child.parents = node
            node.children[fen] = child

        child.count_games += 1
        node = child
    node.game_end = True
    return root_node


def generate_move_tree_branch(root, pgn_list):
    NotImplemented