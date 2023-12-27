# Author: Danny Caspary
# GitHub username: jackie-daytona
# Date: 28 November 2023
# Description: This program runs a variant of chess. In this version, the winner is the first player to capture all of
# an opponent's pieces of one type.

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


class Piece:
    """
    Represents a Piece object on the chess board. Contains color and name data members represented as strings
    and get methods from which the specific piece types will inherit. Rook, Bishop and Queen classes will utilize the
    specific validate methods.
    """
    def __init__(self, color, name):
        self._color = color
        self._name = name

    def get_color(self):
        """Return's the Piece's color"""
        return self._color

    def get_name(self):
        """Return's the Piece's name"""
        return self._name

    def validate_vertical_move(self, board, source_row, source_col, target_row, target_col):
        """Checking for vertical movement up and down the board in the same column"""
        if source_row != target_row and source_col == target_col:
            # moving up the board, towards black's starting side
            if source_row > target_row:
                for index in range(1, source_row-target_row+1):
                    # if we arrive at destination unobstructed return True
                    if source_row - index == target_row:
                        return True
                    # elif there's a piece blocking the way return False
                    elif board[source_row-index][source_col] is not None:
                        return False
            # moving down the board, towards white's starting side
            elif source_row < target_row:
                for index in range(1, target_row-source_row+1):
                    # if we arrive at destination unobstructed return True
                    if source_row+index == target_row:
                        return True
                    # elif there's a piece blocking the way return False
                    elif board[source_row+index][source_col] is not None:
                        return False
        return False

    def validate_horizontal_move(self, board, source_row, source_col, target_row, target_col):
        """Checking for horizontal movement across the board in the same row"""
        if source_row == target_row and source_col != target_col:
            # moving left across the board, from h toward a
            if source_col > target_col:
                for index in range(1, source_col-target_col+1):
                    # if we arrive at the destination unobstructed return True
                    if source_col-index == target_col:
                        return True
                    # elif there's a piece blocking the way return False
                    elif board[source_row][source_col-index] is not None:
                        return False
            # moving right on the board, from a toward h
            elif source_col < target_col:
                for index in range(1, target_col-source_col+1):
                    # if we arrive at the destination unobstructed return True
                    if source_col+index == target_col:
                        return True
                    # elif there's a piece blocking the way return False
                    elif board[source_row][source_col+index] is not None:
                        return False
        return False

    def validate_diagonal_move(self, board, source_row, source_col, target_row, target_col):
        """Checks to see if an inputted diagonal move is legal. Used by the Bishop and Queen objects"""
        if abs(target_col - source_col) == abs(target_row - source_row):
            # if the piece is moving diagonally up and right
            if target_row - source_row < 0 and target_col - source_col > 0:
                for index in range(1, abs(target_col-source_col)+1):
                    if source_row - index == target_row and source_col + index == target_col:
                        return True
                    elif board[source_row-index][source_col+index] is not None:
                        return False
            # if the piece is moving diagonally up and left
            elif target_row - source_row < 0 and target_col - source_col < 0:
                for index in range(1, abs(target_col-source_col)+1):
                    if source_row - index == target_row and source_col - index == target_col:
                        return True
                    elif board[source_row-index][source_col-index] is not None:
                        return False
            # if the piece is moving diagonally down and right
            elif target_row - source_row > 0 and target_col - source_col > 0:
                for index in range(1, abs(target_col-source_col)+1):
                    if source_row + index == target_row and source_col + index == target_col:
                        return True
                    elif board[source_row+index][source_col+index] is not None:
                        return False
            # if the piece is moving diagonally down and left
            elif target_row - source_row > 0 and target_col - source_col < 0:
                for index in range(1, abs(target_col-source_col)+1):
                    if source_row + index == target_row and source_col - index == target_col:
                        return True
                    elif board[source_row+index][source_col-index] is not None:
                        return False
        return False


class King(Piece):
    """Represents a King object on the chess board."""
    def __repr__(self):
        """Return KW or KB for debugging"""
        if self.get_color() == "WHITE":
            return "KW"
        return "KB"

    def validate_move(self, board, source_row, source_col, target_row, target_col):
        """Checks to see if the inputted move for a King is legal"""
        # if the target coordinates are 1 space away from the source coordinates, return true
        if ((target_row == source_row-1 or target_row == source_row+1 or target_row == source_row) and
                (target_col == source_col-1 or target_col == source_col+1 or target_col == source_col)):
            return True
        return False


class Queen(Piece):
    """Represents a Queen object on the chess board."""
    def __repr__(self):
        """Return QW or QB for debugging"""
        if self.get_color() == "WHITE":
            return "QW"
        return "QB"

    def validate_move(self, board, source_row, source_col, target_row, target_col):
        """Determines if the inputted move for a Queen is legal"""
        # if one of the horizontal, vertical or diagonal methods returns True, then it is a valid move for the Queen
        if (self.validate_horizontal_move(board, source_row, source_col, target_row, target_col) or
                self.validate_vertical_move(board, source_row, source_col, target_row, target_col) or
                self.validate_diagonal_move(board, source_row, source_col, target_row, target_col)):
            return True
        return False


class Bishop(Piece):
    """Represents a Bishop object on the chess board"""
    def __repr__(self):
        """Return BW or BB for debugging"""
        if self.get_color() == "WHITE":
            return "BW"
        return "BB"

    def validate_move(self, board, source_row, source_col, target_row, target_col):
        """Determines if the inputted move for a Bishop is legal by calling validate_diagonal_move() from the Piece class."""
        if self.validate_diagonal_move(board, source_row, source_col, target_row, target_col):
            return True
        return False


class Knight(Piece):
    """Represents a Knight object on the chess board."""
    def __repr__(self):
        """Return NW or NB for debugging"""
        if self.get_color() == "WHITE":
            return "NW"
        return "NB"

    def validate_move(self, board, source_row, source_col, target_row, target_col):
        """Checks to see if the inputted move for a Knight is legal"""
        if ((target_row == source_row + 2 or target_row == source_row - 2) and
                (target_col == source_col + 1 or target_col == source_col - 1)):
            return True
        elif ((target_row == source_row + 1 or target_row == source_row - 1) and
              (target_col == source_col + 2 or target_col == source_col - 2)):
            return True
        return False


class Rook(Piece):
    """Represents a Rook object on the chess board."""
    def __repr__(self):
        """Return RW or RB for debugging"""
        if self.get_color() == "WHITE":
            return "RW"
        return "RB"

    def validate_move(self, board, source_row, source_col, target_row, target_col):
        """
        Checks if the inputted move for a Rook is legal by calling validate_horizontal_move() and validate_vertical_move()
        from the parent Piece class
        """
        if (self.validate_horizontal_move(board, source_row, source_col, target_row, target_col) or
                self.validate_vertical_move(board, source_row, source_col, target_row, target_col)):
            return True
        return False


class Pawn(Piece):
    """Represents a Pawn object on the chess board."""
    def __repr__(self):
        """Return PW or PB for debugging"""
        if self.get_color() == "WHITE":
            return "PW"
        return "PB"

    def validate_move(self, board, source_row, source_col, target_row, target_col):
        """
        Determines if the inputted move for a Pawn is legal. Since the Pawn cannot move backwards, this method contains
        separate checks for white and black in three different scenarios: diagonal capturing, first turn movement of one
        or two spaces and regular movement of one space.
        """
        source_piece = board[source_row][source_col]
        target_piece = board[target_row][target_col]
        # capture check for white, if an opponent's piece is diagonally up and left or right one square return True
        if target_row == source_row - 1 and abs(target_col-source_col) == 1 and source_piece.get_color() == "WHITE":
            if target_piece is not None and source_piece.get_color() != target_piece.get_color():
                return True
            return False
        # capture check for black, if an opponent's piece is diagonally down and left or right one square return True
        elif target_row == source_row + 1 and abs(target_col-source_col) == 1 and source_piece.get_color() == "BLACK":
            if target_piece is not None and source_piece.get_color() != target_piece.get_color():
                return True
            return False
        # double move check for white's first turn
        elif source_row == 6 and source_piece.get_color() == "WHITE":
            if target_row == source_row-1 and target_col == source_col:
                # check that the target square is empty to prevent the Pawn from capturing vertically
                if target_piece is None:
                    return True
                return False
            elif target_row == source_row-2 and target_col == source_col:
                # check that the two spaces are empty so the Pawn won't jump or vertically capture any pieces
                if board[source_row-1][source_col] is None and target_piece is None:
                    return True
                else:
                    return False
            return False
        # double move check for black's first turn
        elif source_row == 1 and source_piece.get_color() == "BLACK":
            if target_row == source_row+1 and target_col == source_col:
                # check that the target square is empty to prevent the Pawn from capturing vertically
                if target_piece is None:
                    return True
                return False
            elif target_row == source_row+2 and target_col == source_col:
                # check that the two spaces are empty so the Pawn won't jump or vertically capture any pieces
                if board[source_row+1][source_col] is None and target_piece is None:
                    return True
                else:
                    return False
            return False
        # regular movement vertically up one square for white
        elif target_row == source_row - 1 and source_piece.get_color() == "WHITE":
            # prevent vertical capture
            if target_piece is None:
                return True
            return False
        # regular movement vertically down one square for black
        elif target_row == source_row + 1 and source_piece.get_color() == "BLACK":
            # prevent vertical capture
            if target_piece is None:
                return True
            else:
                return False
        return False
