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
            color, piece = piece_enum_splitter(PieceType.__members__[i].value)
            piece_list.append(Piece(piece, color, (file, rank)))
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
        current_game.castling = None
    else:
        current_game.castling = fen_list[2]
    if fen_list[3] == '-':
        current_game.ep_square = None
    else:
        current_game.ep_square = fen_list[3]
    if fen_list[4]:
        current_game.halfmove = fen_list[4]
    if fen_list[5]:
        current_game.fullmove = fen_list[5]
    
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
            castling = None
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
                    castling = 'K'
            if piece.piece == PieceType.q:
                if 'q' in game_state.castling and move_dest == (3,8):
                    castling = 'Q'
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

        elif new_game_state.player_turn == 'white':
            king_sq = next((p.location for p in new_position if p.piece == PieceType.k), None)
            if king_sq is None:
                raise Exception('King is missing')
            for piece in new_position:
                if king_sq in piece.get_moves(new_game_state, new_position) and piece.color == 'white':
                    legal = False
                    break
        if legal == True:
            move_list.append(move)
    return move_list

                        




def move(game_state, position_list, source, destination, castling, ep, capture, promotion):
    NotImplemented
    #return game_state, piece_list

'''
def move_fen(game_state, piece_list, algebraic):
    player = game_state.player_turn
    if algebraic == '0-0-0':
        if player == 'white':
            for i in piece_list:
                if i.piece == PieceType.K:
                    king = i
                    king.location = (3,1)
                if i.piece == PieceType.R and i.location == (1,1):
                    rook = i
                    rook.location = (4,1)
            castling = game_state.castling
            found = False
            for i in range(0,len(castling)):
                if castling[i].islower():
                    found = True
                    game_state.castling = castling[i:]
                    break
            if found == False:
                game_state.castling = '-'
        if player == 'black':
            for i in piece_list:
                if i.piece == PieceType.k:
                    king = i
                    king.location = (3,8)
                if i.piece == PieceType.r and i.location == (1,8):
                    rook = i
                    rook.location = (4,8)
            castling = game_state.castling
            found = False
            for i in range(0,len(castling)):
                if castling[i].islower():
                    found = True
                    game_state.castling = castling[:i]
                    if castling[:i] == '':
                        castling = '-'
                    break
    if algebraic == '0-0':
        if player == 'white':
            for i in piece_list:
                if i.piece == PieceType.K:
                    king = i
                    king.location = (7,1)
                if i.piece == PieceType.R and i.location == (8,1):
                    rook = i
                    rook.location = (6,1)
            castling = game_state.castling
            found = False
            for i in range(0,len(castling)):
                if castling[i].islower():
                    found = True
                    game_state.castling = castling[i:]
                    break
            if found == False:
                game_state.castling = '-'
        if player == 'black':
            for i in piece_list:
                if i.piece == PieceType.k:
                    king = i
                    king.location = (7,8)
                if i.piece == PieceType.r and i.location == (8,8):
                    rook = i
                    rook.location = (6,8)
            castling = game_state.castling
            found = False
            for i in range(0,len(castling)):
                if castling[i].islower():
                    found = True
                    game_state.castling = castling[:i]
                    if castling[:i] == '':
                        castling = '-'
                    break
    #Search for e.p. - we can remove e.p. from the string since it has no bearing for us:
    algebraic = re.sub('e.p.', '', algebraic)
    
    #Search for + or # and remove them
    algebraic = re.sub('#', '', algebraic)
    algebraic = re.sub('+', ' ', algebraic)

    #Search for promotion:
    promotion = False
    if re.search('=', algebraic):
        promotion = True    
        promotion_string = re.split('=', algebraic)
        algebraic = promotion_string[0]
        promotion_piece = promotion_string[1]
        promotion_piece = PieceType(promotion_piece)
        promotion_piece = promotion_piece.value.split(' ')[1]

    #Handle Captures:
    if re.search('x', algebraic):
        capture_string = re.split('x', algebraic)
        capture_from = capture_string[0]
        capture_location = capture_string[1]
        capture_location = square_to_touple(capture_location)
        for i in piece_list:
            if i.location == capture_location:
                del i


    #Game State updates
    if promotion == True:
        promotion_square = square_to_touple(algebraic[-2:])#MAKE SURE WE HAVE STRIPPED OUT + and # symbols and any other extrenious symbols
        for i in piece_list:
            if i.location == promotion_square:
                i.piece = promotion_piece
    if player == 'black':
        game_state.player_turn = 'white'
        game_state.fullmove += 1
    else:
        game_state.player_turn = 'black'
    
    game_state.halfmove = 1 % (game_state.halfmove+1)

    new_fen = board_obj_to_fen(piece_list, game_state)
    return new_fen
'''