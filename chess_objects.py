from constants import *
from enum import Enum

class PieceType(Enum):
    b = 'black bishop'
    B = 'white bishop'
    k = 'black king'
    K = 'white king'
    n = 'black knight'
    N = 'white knight'
    r = 'black rook'
    R = 'white rook'
    q = 'black queen'
    Q = 'white queen'
    p = 'black pawn'
    P = 'white pawn'

class Files(Enum):
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8


class GameState:
    def __init__(self, castling, player_turn, ep_square=None, halfmove = None, fullmove = None, check = False):
        self.castling = castling
        self.player_turn = player_turn
        self.ep_square = ep_square
        self.halfmove = halfmove
        self.fullmove = fullmove

class Piece:
    def __init__(self, piece, color, location):
        self.piece = piece
        self.color = color
        self.square = None
        self.location = location

    def get_moves(self, game_state, piece_list):
        move_list = []
        pos_to_piece = {p.location: p for p in piece_list}
        castling = False
        if self.piece == PieceType.P or self.piece == PieceType.p:
            if self.color == 'white':
                if self.location[1] == 2:
                    if not pos_to_piece.get((self.location[0], self.location[1]+1)) and not pos_to_piece.get((self.location[0], self.location[1]+2)):
                        move_list.append((self.location[0], self.location[1]+2))
                if game_state.ep_square:
                    targets = [(game_state.ep_square[0]-1,game_state.ep_square[1]-1), (game_state.ep_square[0]+1, game_state.ep_square[1]-1)]
                    if self.location in targets:
                        move_list.append(game_state.ep_square)
                for i in (-1, +1):
                    p = pos_to_piece.get((self.location[0]+i, self.location[1]+1))
                    if p and p.color != self.color:
                        move_list.append((self.location[0]+i, self.location[1]+1))
                if not pos_to_piece.get((self.location[0], self.location[1]+1)):
                    move_list.append((self.location[0], self.location[1]+1))
                
            if self.color == 'black':
                if self.location[1] == 7:
                    if not pos_to_piece.get((self.location[0], self.location[1]-1)) and not pos_to_piece.get((self.location[0], self.location[1]+2)):
                        move_list.append((self.location[0], self.location[1]-2))
                if game_state.ep_square:
                    targets = [(game_state.ep_square[0]-1,game_state.ep_square[1]+1), (game_state.ep_square[0]+1, game_state.ep_square[1]+1)]
                    if self.location in targets:
                        move_list.append(game_state.ep_square)
                for i in (-1, +1):
                    p = pos_to_piece.get((self.location[0]+i, self.location[1]-1))
                    if p and p.color != self.color:
                        move_list.append((self.location[0]+i, self.location[1]-1))
                if not pos_to_piece.get((self.location[0], self.location[1]-1)):
                    move_list.append((self.location[0], self.location[1]-1))

        if self.piece == PieceType.N or self.piece == PieceType.n:
            x, y = self.location
            target_list = [(x+2,y+1), (x+2, y-1), (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2), (x-2, y+1), (x-2, y-1)]
            for target in target_list:
                if not (0<target[0]<9 and 0<target[1]<9):
                    continue
                p = pos_to_piece.get(target)
                if p and p.color == self.color:
                    continue
                move_list.append(target)


        if self.piece == PieceType.B or self.piece == PieceType.b:
            #4 directions to go: += both, -= both, mixed in both
            for i in (1, -1):
                for j in (1, -1):
                    x, y = self.location
                    while True:
                        x+=i
                        y+=j
                        if not 0<x<9:
                            break
                        if not 0<y<9:
                            break
                        blocked = False
                        for piece in piece_list:
                            if piece.location == (x,y):
                                if piece.color != self.color:
                                    move_list.append((x,y))
                                blocked = True
                                break
                        if blocked:
                            break
                        move_list.append((x,y))

        if self.piece == PieceType.R or self.piece == PieceType.r:
            for i in (1, -1):
                x,y = self.location
                #X first
                while True:
                    x+=i
                    if not 0<x<9:
                        break
                    blocked = False
                    for piece in piece_list:
                        if piece.location == (x,y):
                            if piece.color != self.color:
                                move_list.append(piece.location)
                            blocked = True
                            break
                    if blocked:
                        break
                    move_list.append((x,y))
                
                x,y = self.location
                #Now the Y
                while True:
                    y+=i
                    if not 0<y<9:
                        break
                    blocked = False
                    for piece in piece_list:
                        if piece.location == (x,y):
                            if piece.color != self.color:
                                move_list.append(piece.location)
                            blocked = True
                            break
                    if blocked:
                        break
                    move_list.append((x,y))

        if self.piece == PieceType.Q or self.piece == PieceType.q:
            for i in (1, -1):
                for j in (1, -1):
                    x, y = self.location
                    while True:
                        x+=i
                        y+=j
                        if not 0<x<9:
                            break
                        if not 0<y<9:
                            break
                        blocked = False
                        for piece in piece_list:
                            if piece.location == (x,y):
                                if piece.color != self.color:
                                    move_list.append((x,y))
                                blocked = True
                                break
                        if blocked:
                            break
                        move_list.append((x,y))
                
                x,y = self.location
                #X first
                while True:
                    x+=i
                    if not 0<x<9:
                        break
                    blocked = False
                    for piece in piece_list:
                        if piece.location == (x,y):
                            if piece.color != self.color:
                                move_list.append(piece.location)
                            blocked = True
                            break
                    if blocked:
                        break
                    move_list.append((x,y))
                
                x,y = self.location
                #Now the Y
                while True:
                    y+=i
                    if not 0<y<9:
                        break
                    blocked = False
                    for piece in piece_list:
                        if piece.location == (x,y):
                            if piece.color != self.color:
                                move_list.append(piece.location)
                            blocked = True
                            break
                    if blocked:
                        break
                    move_list.append((x,y))

        if self.piece == PieceType.K or self.piece == PieceType.k:
            x,y = self.location
            for i in (-1,0,1):
                if not 0<x+i<9:
                    continue
                for j in (-1,0,1):
                    if not 0<y+j<9:
                        continue
                    if i==0 and j==0:
                        continue
                    p = pos_to_piece.get((x+i, y+j))
                    if p and p.color == self.color:
                        continue
                    move_list.append((x+i, y+j))
            if 'K' in game_state.castling and self.color == 'white':
                blockers = []
                for i in ((7,1), (6,1)):
                    blockers.append(pos_to_piece.get(i))
                if not blockers:
                    move_list.append((7,1))
            if 'k' in game_state.castling and self.color == 'black':
                blockers = []
                for i in ((7,8), (6,8)):
                    blockers.append(pos_to_piece.get(i))
                if not blockers:
                    move_list.append((7,8))
            if 'Q' in game_state.castling and self.color == 'white':
                blockers = []
                for i in ((2,1), (3,1), (4,1)):
                    blockers.append(pos_to_piece.get(i))
                if not blockers:
                    move_list.append((3,1))
            if 'q' in game_state.castling and self.color == 'black':
                blockers = []
                for i in ((2,8), (3,8), (4,8)):
                    blockers.append(pos_to_piece.get(i))
                if not blockers:
                    move_list.append((3,8))

            
        return move_list

    def check_check(self, game_state, piece_list):
        check = False
        move_list = self.get_moves(game_state, piece_list)
        for i in piece_list:
            if self.color == 'white' and i.piece == PieceType.k:
                if i.location in move_list:
                    check = True
            if self.color == 'black' and i.piece == PieceType.K:
                if i.location in move_list:
                    check = True
        return check


