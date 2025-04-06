from piece import *


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
