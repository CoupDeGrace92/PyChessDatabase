# PyChessDatabase
A python database for storing chess games and viewing them on a board

Displaying pieces on the board works from FENs in a given position - the flow is:
FEN -> piece_list, game_state -> move -> new: piece_list, game_state -> new: FEN
                              ->graphically interpret
In this way we can use pgn files to create states of FENs as parent/children nodes for a given game.  In the last move of the game, we store information about the game itself.

We use open-source piece images and a board rendered with pygame.

    - NOT IMPLEMENTED: Moving pieces to create game
    - Read pgn files into a database
    - Write database file into a pgn file
    - Position searches, player searches, opening searches, result searches/combanative search algo
    - External engine evaluation
    - Use Lichess API to import games from a player
    - Truncation for database size purposes/opening depth purposes