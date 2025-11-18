from constants import *

def pgn_to_move_list(pgn):
    fen_obj = re.search(r'\[FEN\s+"([^"]*)"\]', pgn)
    if fen_obj:
        fen = fen_obj.group(1) 
    else:
        fen = DEFAULT
