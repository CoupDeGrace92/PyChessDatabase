from chess_objects import *
import re
import copy

def piece_enum_splitter(string):
    obj_list = string.split()
    color = obj_list[0]
    piece = obj_list[1]
    return color, piece

def fen_to_board_obj(fen):
    piece_list = []
    rank = 8
    file = 1
    fen_list = fen.split()
    current_game = GameState(None, None)
    for i in fen_list[0]:  #This is the piece location part of the FEN string
        if i in PieceType.__members__:
            enum_piece = PieceType[i]          # the Enum member
            color = 'white' if i.isupper() else 'black'
            piece_list.append(Piece(enum_piece, color, (file, rank)))
            file += 1
        elif i=="/":
            rank -= 1
            file = 1
        elif i.isdigit():
            file += int(i)
        else:
            raise  Exception(f"Unrecognized character in fen string piece location: {i}")
    if fen_list[1] == 'w':
        current_game.player_turn = 'white'
    elif fen_list[1] == 'b':
        current_game.player_turn = 'black'
    else:
        raise Exception(f"Unrecognized character in fen string player turn: {fen_list[2]}")
    if fen_list[2] == '-':
        current_game.castling = ''
    else:
        current_game.castling = fen_list[2]
    if fen_list[3] == '-':
        current_game.ep_square = None
    else:
        current_game.ep_square = fen_list[3]
    if fen_list[4]:
        current_game.halfmove = int(fen_list[4])
    if fen_list[5]:
        current_game.fullmove = int(fen_list[5])
    
    return current_game, piece_list
        
def board_obj_to_fen(piece_list, game_state):
    fen_string = ''
    empty = 0
    for i in range(8):
        for j in range(8):
            y_index = 8-i
            x_index = j+1
            piece = next((obj for obj in piece_list if obj.location == (x_index,y_index)), None)
            if piece:
                piece_label = piece.color + ' ' + piece.piece
                piece_name = PieceType(piece_label)
                if empty !=0:
                    fen_string += str(empty)
                fen_string += piece_name.name
                empty = 0
            else:
                empty += 1
        if empty != 0:
            fen_string += str(empty)
            empty = 0
        if i!=7:
            fen_string += '/'
    fen_string += ' '
    fen_string += game_state.player_turn[0]
    fen_string += ' '
    if game_state.castling:
        fen_string += game_state.castling
    else:
        fen_string += '-'
    fen_string += ' '
    if game_state.ep_square:
        fen_string += game_state.ep_square
    else:
        fen_string += '-'
    fen_string += ' '
    fen_string += game_state.halfmove
    fen_string += ' '
    fen_string += game_state.fullmove
    return fen_string
    
def square_to_touple(square_string):
    if len(square_string) > 2:
        raise Exception(f'Incorrectly formatted square name: {square_string}')
    file = Files(square_string[0])
    square_touple = (file.name, square_string[1])
    return square_touple

def legal_moves(game_state, piece_list):
    move_list = []
    psuedo_move_list = []
    pos_to_piece = {p.location: p for p in piece_list}
    to_move_piece_list = []
    for piece in piece_list:
        if piece == game_state.player_turn:
            to_move_piece_list.append(piece)
    for piece in to_move_piece_list:
        dest_list = piece.get_moves(game_state, to_move_piece_list)
        for move_dest in dest_list:
            source = piece.location
            castling = ''
            ep = False
            capture = False
            promotion = None
            if piece.piece == PieceType.K:
                if 'K' in game_state.castling and move_dest == (7,1):
                    castling = 'K'
            if piece.piece == PieceType.Q:
                if 'Q' in game_state.castling and move_dest == (3,1):
                    castling = 'Q'
            if piece.piece == PieceType.k:
                if 'k' in game_state.castling and move_dest == (7,8):
                    castling = 'k'
            if piece.piece == PieceType.q:
                if 'q' in game_state.castling and move_dest == (3,8):
                    castling = 'q'
            if piece.piece == PieceType.P:
                if move_dest == game_state.ep_square:
                    capture = True
                    ep = True
                if move_dest[0] == 8:
                    promotion = True
            if piece.piece == PieceType.p:
                if move_dest == game_state.ep_square:
                    capture = True
                    ep = True
                if move_dest[0] == 1:
                    promotion = True
            occupied = pos_to_piece.get(move_dest)
            if occupied:
                capture = True
            psuedo_move_list.append((piece.piece, source, move_dest, castling, ep, capture, promotion))
    for m in psuedo_move_list:
        original_position = copy.deepcopy(piece_list) #Deepcopy of the original position
        original_gamestate = copy.deepcopy(game_state) #Deepcopy of the original gamestate object
        new_game_state, new_position = move(original_gamestate, original_position, m[1], m[2], m[3], m[4], m[5], m[6])
        legal = True

        if new_game_state.player_turn == 'black':
            king_sq = next((p.location for p in new_position if p.piece == PieceType.K), None)
            if king_sq is None:
                raise Exception('King is missing')
            for piece in new_position:
                if king_sq in piece.get_moves(new_game_state, new_position) and piece.color == 'black':
                    legal = False
                    break
                if castling == 'K':
                    target_square = (6,1)
                    if target_square in piece.get_moves(new_game_state, new_position) and piece.color == 'black':
                        legal = False
                        break
                if castling == 'Q':
                    target_square = (4,1)
                    if target_square in piece.get_moves(new_game_state, new_position) and piece.color == 'black':
                        legal = False
                        break

        elif new_game_state.player_turn == 'white':
            king_sq = next((p.location for p in new_position if p.piece == PieceType.k), None)
            if king_sq is None:
                raise Exception('King is missing')
            for piece in new_position:
                if king_sq in piece.get_moves(new_game_state, new_position) and piece.color == 'white':
                    legal = False
                    break
                if castling == 'k':
                    target_square = (6,8)
                    if target_square in piece.get_moves(new_game_state, new_position) and piece.color == 'white':
                        legal = False
                        break
                if castling == 'q':
                    target_square = (4,8)
                    if target_square in piece.get_moves(new_game_state, new_position) and piece.color == 'white':
                        legal = False
                        break

        if legal == True:
            move_list.append(move)
    return move_list


def move(game_state, position_list, source, destination, castling, ep, capture, promotion):  #Note that promotion is a PieceType Enum
    moved_piece = next((piece for piece in position_list if piece.location == source), None)
    captured_piece = None
    king_rook_move = False
    queen_rook_move = False
    king_rook_capture = False
    queen_rook_capture = False

    if moved_piece == None:
        return None, None

    if moved_piece.piece == PieceType.R and source == (1,1):
        queen_rook_move = True
    elif moved_piece.piece == PieceType.R and source == (8,1):
        king_rook_move = True
    elif moved_piece.piece == PieceType.r and source == (1,8):
        queen_rook_move = True
    elif moved_piece.piece == PieceType.r and source == (8,8):
        king_rook_move = True

    if capture == True:
        captured_piece_location = destination
        if ep == True:
            if game_state.player_turn == 'white':
                captured_piece_location = (destination[0], destination[1]-1)
            else:
                captured_piece_location = (destination[0], destination[1]+1)
        captured_piece = next((piece for piece in position_list if piece.location == captured_piece_location), None)
        if captured_piece.piece == PieceType.R:
            if captured_piece.location == (1,1):
                queen_rook_capture = True
            if captured_piece.location == (8,1):
                king_rook_capture = True
        if captured_piece.piece == PieceType.r:
            if captured_piece.location == (1,8):
                queen_rook_capture = True
            if captured_piece.location == (8,8):
                king_rook_capture = True
    if captured_piece:
        position_list.remove(captured_piece)
    moved_piece.location = destination
    if promotion:
        moved_piece.piece = promotion
    if castling == 'k':
        rook_to_move = next((piece for piece in position_list if piece.location == (8,8)), None)
        if rook_to_move == None:
            raise Exception('No rook to castle with')
        rook_to_move.location = (6,8)
    if castling == 'q':
        rook_to_move = next((piece for piece in position_list if piece.location == (1,8)), None)
        if rook_to_move == None:
            raise Exception('No rook to castle with')
        rook_to_move.location = (4,8)
    if castling == 'K':
        rook_to_move = next((piece for piece in position_list if piece.location == (8,1)), None)
        if rook_to_move == None:
            raise Exception('No rook to castle with')
        rook_to_move.location = (6,1)
    if castling == 'Q':
        rook_to_move = next((piece for piece in position_list if piece.location == (1,1)), None)
        if rook_to_move == None:
            raise Exception('No rook to castle with')
        rook_to_move.location = (4,1)
    
    game_state.ep_square = None
    if moved_piece.piece == PieceType.P:
        if destination[1]-source[1] == 2:
            game_state.ep_square = (destination[0], destination[1]-1)
    elif moved_piece.piece == PieceType.p:
        if source[1] - destination[1] == 2:
            game_state.ep_square = (destination[0], destination[1]+1)
    
    if game_state.player_turn == 'black':
        game_state.player_turn = 'white'
        game_state.fullmove += 1

    elif game_state.player_turn == 'white':
        game_state.player_turn = 'black'

    if capture or moved_piece.piece in (PieceType.P, PieceType.p) or promotion:
        game_state.halfmove = 0
    else:
        game_state.halfmove += 1

    castling_string = game_state.castling
    if moved_piece.piece == PieceType.K:
        castling_string = castling_string.replace('K','')
        castling_string = castling_string.replace('Q','')
    if moved_piece.piece == PieceType.k:
        castling_string = castling_string.replace('k', '')
        castling_string = castling_string.replace('q', '')
    if king_rook_move == True:
        if moved_piece.color == 'white':
            castling_string = castling_string.replace('K','')
        else:
            castling_string = castling_string.replace('k')
    if queen_rook_move == True:
        if moved_piece.color == 'white':
            castling_string = castling_string.replace('Q', '')
        else:
            castling_string = castling_string.replace('q', '')
    if king_rook_capture == True:
        if moved_piece.color == 'white':
            castling_string = castling_string.replace('k', '')
        else:
            castling_string = castling_string.replace('K', '')
    if queen_rook_capture == True:
        if moved_piece.color == 'white':
            castling_string = castling_string.replace('q', '')
        else:
            castling_string = castling_string.replace('Q', '')

    game_state.castling = castling_string
    return game_state, position_list

def algebraic_to_move(algebraic, game_state, position_list):
    source = None
    destination = None
    castling = ''
    ep = False
    capture = False
    promotion = None


    algebraic = algebraic.strip()
    algebraic = algebraic.strip('+#')

    if algebraic == '0-0-0':
        if game_state.player_turn == 'white':
            castling = 'Q'
            source = (5,1)
            destination = (3,1)
        else:
            castling = 'q'
            source = (5,8)
            destination = (3,8)
    elif algebraic == '0-0':
        if game_state.player_turn == 'white':
            castling = 'K'
            source = (5,1)
            destination = (7,1)
        else:
            castling = 'k'
            source = (5,8)
            destination = (7,8)
    else:
        if re.search('=', algebraic):
            algebraic_list = algebraic.split('=')
            algebraic = algebraic_list[0]
            promotion = algebraic_list[1]
            if game_state.player_turn == 'white':
                promotion = promotion.upper()
            if game_state.player_turn == 'black':
                promotion = promotion.lower()
            promotion = PieceType[promotion]

        if re.search('e.p.', algebraic):
            ep = True
            algebraic = algebraic.replace('e.p.', '')
        if re.search('x', algebraic):
            capture = True
            algebraic = algebraic.replace('x', '')
        if algebraic[0].islower():  #Dealing with a pawn move
            if algebraic[1].isnumeric(): #Advance not capture
                destination = (Files[algebraic[0]].value, int(algebraic[1]))
                if int(algebraic[1]) == 4 and game_state.player_turn == 'white':
                    one_square = False
                    for p in position_list:
                        if p.location == (Files[algebraic[0]].value,3):
                            one_square = True
                            break
                    if one_square == True:
                        source = (Files[algebraic[0]].value,3)
                    else:
                        source = (Files[algebraic[0]].value,2)
                elif int(algebraic[1]) == 5 and game_state.player_turn == 'black':
                    one_square = False
                    for p in position_list:
                        if p.location == (Files[algebraic[0]].value, 6):
                            one_square = True
                            break
                    if one_square == True:
                        source = (Files[algebraic[0]].value, 6)
                    else:
                        source = (Files[algebraic[0]].value, 7)
                else:
                    if game_state.player_turn == 'white':
                        source = (Files[algebraic[0]].value, int(algebraic[1])-1)
                    else:
                        source = (Files[algebraic[0]].value, int(algebraic[1])+1)
            else:
                if game_state.player_turn == 'white':
                    source = (Files[algebraic[0]].value, int(algebraic[2])-1)
                else:
                    source = (Files[algebraic[0]].value, int(algebraic[2])+1)
                destination = (Files[algebraic[1]].value, int(algebraic[2]))
        else:
            if len(algebraic) == 3:
                destination = (Files[algebraic[1]].value, int(algebraic[2]))
                if game_state.player_turn == 'white':
                    target_piece = PieceType[algebraic[0].upper()]
                else:
                    target_piece = PieceType[algebraic[0].lower()]
                for p in position_list:
                    if destination in p.get_moves(game_state, position_list) and p.piece == target_piece:
                        psuedo_position = copy.deepcopy(position_list)
                        psuedo_gamestate = copy.deepcopy(game_state)
                        psuedo_gamestate, psuedo_position = move(psuedo_gamestate, psuedo_position, p.location, destination, castling, ep, capture, promotion)
                        move_legal = True
                        for piece in psuedo_position:
                            if psuedo_gamestate.player_turn == 'white':
                                if piece.piece == PieceType.k:
                                    target_location = piece.location
                                    break
                            else:
                                if piece.piece == PieceType.K:
                                    target_location = piece.location
                                    break
                        for piece in psuedo_position:
                            if psuedo_gamestate.player_turn == piece.color:
                                if target_location in p.get_moves(psuedo_gamestate, psuedo_position):
                                    move_legal = False
                                    break
                        if move_legal == True:
                            source = p.location
            
            if len(algebraic) == 4:
                if algebraic[1].isnumeric():
                    destination = (Files[algebraic[2]].value, int(algebraic[3]))
                    for p in position_list:
                        if destination in p.get_moves(game_state, position_list) and p.location[1] == int(algebraic[1]) and p.piece == target_piece:
                            psuedo_position = copy.deepcopy(position_list)
                            psuedo_gamestate = copy.deepcopy(game_state)
                            psuedo_gamestate, psuedo_position = move(psuedo_gamestate, psuedo_position, p.location, destination, castling, ep, capture, promotion)
                            move_legal = True
                            for piece in psuedo_position:
                                if psuedo_gamestate.player_turn == 'white':
                                    if piece.piece == PieceType.k:
                                        target_location = piece.location
                                        break
                                else:
                                    if piece.piece == PieceType.K:
                                        target_location = piece.location
                                        break
                            for piece in psuedo_position:
                                if psuedo_gamestate.player_turn == piece.color:
                                    if target_location in p.get_moves(psuedo_gamestate, psuedo_position):
                                        move_legal = False
                                        break
                            if move_legal == True:
                                source = p.location
                else:
                    destination = (Files[algebraic[2]].value, int(algebraic[3]))
                    for p in position_list:
                        if destination in p.get_moves(game_state, position_list) and p.location[1] == Files[algebraic[1]].value and p.piece == target_piece:
                            psuedo_position = copy.deepcopy(position_list)
                            psuedo_gamestate = copy.deepcopy(game_state)
                            psuedo_gamestate, psuedo_position = move(psuedo_gamestate, psuedo_position, p.location, destination, castling, ep, capture, promotion)
                            move_legal = True
                            for piece in psuedo_position:
                                if psuedo_gamestate.player_turn == 'white':
                                    if piece.piece == PieceType.k:
                                        target_location = piece.location
                                        break
                                else:
                                    if piece.piece == PieceType.K:
                                        target_location = piece.location
                                        break
                            for piece in psuedo_position:
                                if psuedo_gamestate.player_turn == piece.color:
                                    if target_location in p.get_moves(psuedo_gamestate, psuedo_position):
                                        move_legal = False
                                        break
                            if move_legal == True:
                                source = p.location

            if len(algebraic) == 5:
                destination = (Files[algebraic[3]].value, int(algebraic[4]))
                source = (Files[algebraic[1]].value, int(algebraic[2]))

    return source, destination, castling, ep, capture, promotion

                                

def check_checkmate(game_state, position_list):
    if legal_moves(game_state, position_list) == []:
        return True
    return False