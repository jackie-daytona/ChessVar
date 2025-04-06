from subpieces import *


class ChessVar:
    """
    Simulates the chess variant game. Contains seven data members:
    * game_state: a string representing the game's status, can be "UNFINISHED", "BLACK_WON" or "WHITE_WON"
    * turn: a string representing whose turn it is, can be "WHITE" or "BLACK"
    * rows: a string representing the numbered rows used in chess notation. this is used to get the index values
                for each move inputted in the make_move() method
    * columns: a string representing the letters columns used in chess notation. this is used to get the row values
                for each move inputted in the make_move() method
    * white_count, black_count: dictionaries representing the remaining number of pieces for each player
    * board: a 2d array representing the chess board
    """
    def __init__(self):
        self._game_state = "UNFINISHED"
        self._turn = "WHITE"
        self._rows = "87654321"
        self._columns = "abcdefgh"
        self._white_count = {
            "PAWN": 8,
            "ROOK": 2,
            "KNIGHT": 2,
            "BISHOP": 2,
            "QUEEN": 1,
            "KING": 1
        }
        self._black_count = {
            "PAWN": 8,
            "ROOK": 2,
            "KNIGHT": 2,
            "BISHOP": 2,
            "QUEEN": 1,
            "KING": 1
        }
        self._board = [
            # row 0
            [Rook("BLACK", "ROOK"), Knight("BLACK", "KNIGHT"), Bishop("BLACK", "BISHOP"), Queen("BLACK", "QUEEN"),
             King("BLACK", "KING"), Bishop("BLACK", "BISHOP"), Knight("BLACK", "KNIGHT"), Rook("BLACK", "ROOK")],
            # row 1
            [Pawn("BLACK", "PAWN"), Pawn("BLACK", "PAWN"), Pawn("BLACK", "PAWN"), Pawn("BLACK", "PAWN"),
             Pawn("BLACK", "PAWN"), Pawn("BLACK", "PAWN"), Pawn("BLACK", "PAWN"), Pawn("BLACK", "PAWN")],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            # row 6
            [Pawn("WHITE", "PAWN"), Pawn("WHITE", "PAWN"), Pawn("WHITE", "PAWN"), Pawn("WHITE", "PAWN"),
             Pawn("WHITE", "PAWN"), Pawn("WHITE", "PAWN"), Pawn("WHITE", "PAWN"), Pawn("WHITE", "PAWN")],
            # row 7
            [Rook("WHITE", "ROOK"), Knight("WHITE", "KNIGHT"), Bishop("WHITE", "BISHOP"), Queen("WHITE", "QUEEN"),
             King("WHITE", "KING"), Bishop("WHITE", "BISHOP"), Knight("WHITE", "KNIGHT"), Rook("WHITE", "ROOK")]
        ]

    def get_game_state(self):
        """Returns game_state"""
        return self._game_state

    def set_game_state(self, new_state):
        """Updates the game_state if a player has won"""
        self._game_state = new_state

    def get_board(self):
        """Returns the board data member"""
        return self._board

    def get_turn(self):
        """Returns the player whose turn it is"""
        return self._turn

    def make_move(self, source, target):
        """Moves the piece object located at source to the target on the board data member."""
        # get board coordinates from the source and target strings
        source_row = 0
        source_col = 0
        target_row = 0
        target_col = 0
        # getting the row index values for both source and target
        for index, value in enumerate(self._rows):
            if source[1] == value:
                source_row = index
            if target[1] == value:
                target_row = index
        # getting the column index values for both source and target
        for index, value in enumerate(self._columns):
            if source[0] == value:
                source_col = index
            if target[0] == value:
                target_col = index

        # call validate_move() to determine if the inputted move is legal
        if self.validate_move(self._board, source_row, source_col, target_row, target_col) is False:
            return False

        # the move is valid at this point, so create temporary variables and execute the move
        origin_square = self._board[source_row][source_col]
        destination_square = self._board[target_row][target_col]
        # if the target square is empty, move the piece to the destination square and empty origin square
        if destination_square is None:
            self._board[target_row][target_col] = origin_square
            self._board[source_row][source_col] = None

        # else if the target square is occupied by an opposing piece (and is not empty), capture the piece
        elif destination_square.get_color() != self._turn and destination_square is not None:
            if self._turn == "WHITE":
                for key in self._black_count:
                    if key == destination_square.get_name():
                        self._black_count[key] -= 1
            else:
                for key in self._white_count:
                    if key == destination_square.get_name():
                        self._white_count[key] -= 1
            self._board[target_row][target_col] = origin_square
            self._board[source_row][source_col] = None

        # update the game state if a player has won
        # if a piece is white's count dict is down to zero, black has won
        for value in self._white_count.values():
            if value == 0:
                self.set_game_state("BLACK_WON")
        # if a piece in black's count dict is at zero, white has won
        for value in self._black_count.values():
            if value == 0:
                self.set_game_state("WHITE_WON")

        # update whose turn it is and return True to complete the move
        if self._turn == "WHITE":
            self._turn = "BLACK"
        else:
            self._turn = "WHITE"
        return True

    def validate_move(self, board, source_row, source_col, target_row, target_col):
        """
        Helper method for make_move. Checks whether the parameters are a legal chess move.
        * board: 2d array representing the current board state
        * source_row, source_col: coordinates derived in make_move() from the inputted chess notation for a piece's
                                        starting position
        * target_row, target_col: coordinates derived in make_move() from the inputted chess notation for a piece's
                                        finishing position
        """
        source_piece = self._board[source_row][source_col]
        target_piece = self._board[target_row][target_col]
        # if the piece on the starting square doesn't belong to the player whose turn it is, return False
        if source_piece is not None and source_piece.get_color() != self._turn:
            return False
        # if the piece on the destination square is the same color as the player whose turn it is, return False
        if target_piece is not None and target_piece.get_color() == self._turn:
            return False
        # if the game has already been won, return False
        elif self._game_state != "UNFINISHED":
            return False
        # if that piece object's move is invalid, return False
        elif (source_piece is not None and
              source_piece.validate_move(self._board, source_row, source_col, target_row, target_col)) is False:
            return False
        return True

    def display(self):
        """Prints the current state of the board."""
        for index in self._board:
            print(index)

