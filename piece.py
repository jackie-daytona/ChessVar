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
