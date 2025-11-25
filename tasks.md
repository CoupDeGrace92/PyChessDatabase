Dynamic game list
    -Move rectangle the size of the board, width of 2-3 squares.  Move num(FEN string has this), white move, black move
    -back arrow removes previous move (candidates below the box)
    -if we get to more moves than can fit - shift moves up (removing from beggining)
        - METHOD - save algebraic moves, update text_move_tree to return the algebraic move, back arrow removes previous move (OR highlights current move)
        - One option - list that contains touples that represent each line, once len > # lines, slice [1:], save as second list so we can go backwards too
Multiple child moves - children nodes are a touple (move, node), candidate moves below game list, up down arrow to move between them (display max n)
