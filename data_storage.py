default = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

class FEN:
    def __init__(self, FEN):
        self.position = FEN

class PGN:
    def __init__(self, move_list, FEN=default):
        self.game = move_list
        self.starting_position = FEN

class Database:
    def __init__(self, move_list):
        #self.starting_tree = generate_move_tree(move_list)
        starting_position = PositionNode(default)

        def add_game(pgn, game_object):
            temp_tree = generate_move_tree(move_list)
            if temp_tree[0] != default:
                raise Exception('Invalid starting position - non-default starting positions not implemented')
                #search_for(temp_tree[0])
            current_node = starting_position
            for i in temp_tree:
                if i not in current_node.children:
                    current_node.children.append(i)
                current_node = i
            current_node.game_end = True

class PositionNode:
    def __init__(self, fen):
        self.fen = fen
        self.children = None
        self.parents = None
        self.count_games = 0
        self.game_end = False

class GameObject:
    def __init__(self, black_player='NN', white_player='NN', result='?', date='?'):
        self.black = black_player
        self.white = white_player
        self.result = result
        self.date = date