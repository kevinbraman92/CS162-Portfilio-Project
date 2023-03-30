class InvalidSquare(IndexError):
    """
     This exception is raised within the GameLogic object when a player makes an out-of-bounds move.
     Used by the following methods: get_checker_details
    """
    pass


class GameLogic:
    """Represents the movement and capture logic for a game of checkers."""

    def __init__(self):
        """
        Constructor method that takes no parameters.

        The following private data members are initialized:

        game_won        = if any player captures 12 pieces, the game is won. Defaults to boolean False
        players         = initialized as an empty dictionary
        board           = creates a list of lists that represents the board. 12 squares on the top have the string
                          "White", on the bottom 12 squares have the string "Black". These are the pieces used by the
                          players. The remaining spaces are element positions containing noneType None.
        """
        self._capture_state = False
        self._players = {}
        self._board = [[None, "White", None, "White", None, "White", None, "White"],
                       ["White", None, "White", None, "White", None, "White", None],
                       [None, "White", None, "White", None, "White", None, "White"],
                       [None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None],
                       ["Black", None, "Black", None, "Black", None, "Black", None],
                       [None, "Black", None, "Black", None, "Black", None, "Black"],
                       ["Black", None, "Black", None, "Black", None, "Black", None]]

    def get_checker_details(self, square_location):
        """
        This class method takes one parameter:
        square_location      = a tuple in (x, y), representing a position on the board

        This method accesses the board data member and returns the element accessed by the tuple.
        If a position outside the board is chosen, an InvalidSquare Exception is raised.
        """
        row, column = square_location[0], square_location[1]

        if row > 7 or column > 7:
            raise InvalidSquare

        return self._board[row][column]

    def upgrade_piece(self, player_name, destination_square_location):
        """
        This class method takes two parameters:
        player_name                     = a string containing the player's name
        destination_square_location     = a tuple in (x, y), representing a destination square on the board

        This class method upgrades a pawn piece into a king, and a king into a triple king if the piece is in the
        appropriate position:

        'Black' pawns upgrade when in row 0 and 'Black_kings' upgrade in row 7.
        'White' pawns upgrade when in row 7 and 'White_kings' upgrade in row 0.

        """

        destination_row, destination_column = destination_square_location[0], destination_square_location[1]

        # Upgrade piece
        if "Black" in self._board[0]:
            self._players[player_name].add_king()
            self._board[destination_row][destination_column] = "Black_king"
        elif "Black_king" in self._board[7]:
            self._players[player_name].remove_king()
            self._players[player_name].add_triple_king()
            self._board[destination_row][destination_column] = "Black_Triple_King"
        elif "White" in self._board[7]:
            self._players[player_name].add_king()
            self._board[destination_row][destination_column] = "White_king"
        elif "White_king" in self._board[0]:
            self._players[player_name].remove_king()
            self._players[player_name].add_triple_king()
            self._board[destination_row][destination_column] = "White_Triple_King"

    def can_capture(self, square_location):
        """
        This method takes one parameter:
        square_location     = a tuple in (x, y), representing a position on the board

        This method checks if a piece in its current position can capture. If it can, this method returns True,
        otherwise it returns False. There is different capture logic depending on the piece in question:

        Pawns can capture up-left or up-right if 'Black', down-left or down-right if 'White'.

        Kings can capture up-left, up-right, down-left, & down-right. In addition, they do not have to be next to a
        piece to capture, as long as they are on the same diagonal.

        Triple kings can do everything a king can, as well as double capture.
        """
        start = self.get_checker_details(square_location)
        row, column = square_location[0], square_location[1]
        white_list, black_list = ["White", "White_king", "White_Triple_King"], ["Black", "Black_king",
                                                                                "Black_Triple_King"]
        # Black pawn capture logic
        if start == "Black":
            if column == 0 and row != 1:
                # Up-right
                if self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
            elif column == 7:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
            elif column == 1:
                # Up-right
                if self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
            elif column == 6 and row != 1:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
            elif row != 1:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                if self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
            else:
                return False
        # White pawn capture logic
        elif start == "White":
            if column == 7 and row != 6:
                # Down-left
                if self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
            elif column == 0:
                # Down-right
                if self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif column == 1 and row != 6:
                # Down-right
                if self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif column == 6 and row != 6:
                # Down-left
                if self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
            elif row != 6:
                # Down-left
                if self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                if self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            else:
                return False
        # Black king's capture logic
        elif start == "Black_king":
            if row == 7 and column == 0:
                # Up-right
                if self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] is None:
                    return True
                elif self._board[row - 5][column + 5] in white_list and self._board[row - 6][column + 6] is None:
                    return True
                elif self._board[row - 6][column + 6] in white_list and self._board[row - 7][column + 7] is None:
                    return True
            elif row == 7 and column == 2:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] is None:
                    return True
            elif row == 7 and column == 4:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
            elif row == 7 and column == 6:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in white_list and self._board[row - 5][column - 5] is None:
                    return True
                elif self._board[row - 5][column - 5] in white_list and self._board[row - 6][column - 6] is None:
                    return True
            elif row == 6 and column == 1:
                # Up-right
                if self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] is None:
                    return True
                elif self._board[row - 5][column + 5] in white_list and self._board[row - 6][column + 6] is None:
                    return True
            elif row == 6 and column == 3:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
            elif row == 6 and column == 5:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in white_list and self._board[row - 5][column - 5] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
            elif row == 6 and column == 7:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in white_list and self._board[row - 5][column - 5] is None:
                    return True
                elif self._board[row - 5][column - 5] in white_list and self._board[row - 6][column - 6] is None:
                    return True
            elif row == 5 and column == 0:
                # Up-right
                if self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 2:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 4:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 6:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in white_list and self._board[row - 5][column - 5] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
            elif row == 4 and column == 1:
                # Up-right
                if self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 4 and column == 3:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 4 and column == 5:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 4 and column == 7:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
            elif row == 3 and column == 0:
                # Up-right
                if self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 3 and column == 2:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 3 and column == 4:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 3 and column == 6:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
            elif row == 2 and column == 1:
                # Up-right
                if self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in white_list and self._board[row + 5][column + 5] is None:
                    return True
            elif row == 2 and column == 3:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 2 and column == 5:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 2 and column == 7:
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] is None:
                    return True
            elif row == 1 and column == 0:
                # Down-right
                if self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in white_list and self._board[row + 5][column + 5] is None:
                    return True
                elif self._board[row + 5][column + 5] in white_list and self._board[row + 6][column + 6] is None:
                    return True
            elif row == 1 and column == 2:
                # Down-left
                if self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in white_list and self._board[row + 5][column + 5] is None:
                    return True
            elif row == 1 and column == 4:
                # Down-left
                if self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 1 and column == 6:
                # Down-left
                if self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] is None:
                    return True
                elif self._board[row + 5][column - 5] in white_list and self._board[row + 6][column - 6] is None:
                    return True
            elif row == 0 and column == 1:
                # Down-right
                if self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in white_list and self._board[row + 5][column + 5] is None:
                    return True
                elif self._board[row + 5][column + 5] in white_list and self._board[row + 6][column + 6] is None:
                    return True
            elif row == 0 and column == 3:
                # Down-left
                if self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 0 and column == 5:
                # Down-left
                if self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 0 and column == 7:
                # Down-left
                if self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] is None:
                    return True
                elif self._board[row + 5][column - 5] in white_list and self._board[row + 6][column - 6] is None:
                    return True
                elif self._board[row + 6][column - 6] in white_list and self._board[row + 7][column - 7] is None:
                    return True
        elif start == "Black_Triple_King":
            if row == 7 and column == 0:
                # Up-right double
                if (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                        white_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] in
                      white_list and self._board[row - 4][column + 4] is None):
                    return True
                elif (self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] in
                      white_list and self._board[row - 5][column + 5] is None):
                    return True
                elif (self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] in
                      white_list and self._board[row - 6][column + 6] is None):
                    return True
                elif (self._board[row - 5][column + 5] in white_list and self._board[row - 6][column + 6] in
                      white_list and self._board[row - 7][column + 7]) is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] is None:
                    return True
                elif self._board[row - 5][column + 5] in white_list and self._board[row - 6][column + 6] is None:
                    return True
                elif self._board[row - 6][column + 6] in white_list and self._board[row - 7][column + 7] is None:
                    return True
            elif row == 7 and column == 2:
                # Up-right double
                if (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                        white_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] in
                      white_list and self._board[row - 4][column + 4] is None):
                    return True
                elif (self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] in
                      white_list and self._board[row - 5][column + 5] is None):
                    return True
                elif (self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] in
                      white_list and self._board[row - 6][column + 6] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] is None:
                    return True
            elif row == 7 and column == 4:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] in
                      white_list and self._board[row - 4][column - 4] is None):
                    return True
                # Up-right double
                elif (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                      white_list and self._board[row - 3][column + 3] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
            elif row == 7 and column == 6:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] in
                      white_list and self._board[row - 4][column - 4] is None):
                    return True
                elif (self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] in
                      white_list and self._board[row - 5][column - 5] is None):
                    return True
                elif (self._board[row - 4][column - 4] in white_list and self._board[row - 5][column - 5] in
                      white_list and self._board[row - 6][column - 6] is None):
                    return True
                    # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in white_list and self._board[row - 5][column - 5] is None:
                    return True
                elif self._board[row - 5][column - 5] in white_list and self._board[row - 6][column - 6] is None:
                    return True
            elif row == 6 and column == 1:
                # Up-right double
                if (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                        white_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] in
                      white_list and self._board[row - 4][column + 4] is None):
                    return True
                elif (self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] in
                      white_list and self._board[row - 5][column + 5] is None):
                    return True
                elif (self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] in
                      white_list and self._board[row - 6][column + 6] is None):
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] is None:
                    return True
                elif self._board[row - 5][column + 5] in white_list and self._board[row - 6][column + 6] is None:
                    return True
            elif row == 6 and column == 3:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                # Up-right double
                elif (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                      white_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] in
                      white_list and self._board[row - 4][column + 4] is None):
                    return True
            elif row == 6 and column == 5:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] in
                      white_list and self._board[row - 4][column - 4] is None):
                    return True
                elif (self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] in
                      white_list and self._board[row - 5][column - 5] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in white_list and self._board[row - 5][column - 5] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
            elif row == 6 and column == 7:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] in
                      white_list and self._board[row - 4][column - 4] is None):
                    return True
                elif (self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] in
                      white_list and self._board[row - 5][column - 5] is None):
                    return True
                elif (self._board[row - 4][column - 4] in white_list and self._board[row - 5][column - 5] in
                      white_list and self._board[row - 6][column - 6] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in white_list and self._board[row - 5][column - 5] is None:
                    return True
                elif self._board[row - 5][column - 5] in white_list and self._board[row - 6][column - 6] is None:
                    return True
            elif row == 5 and column == 0:
                # Up-right double
                if (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                        white_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] in
                      white_list and self._board[row - 4][column + 4] is None):
                    return True
                elif (self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] in
                      white_list and self._board[row - 5][column + 5] is None):
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 2:
                # Up-right double
                if (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                        white_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] in
                      white_list and self._board[row - 4][column + 4] is None):
                    return True
                elif (self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] in
                      white_list and self._board[row - 5][column + 5] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in white_list and self._board[row - 5][column + 5] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 4:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] in
                      white_list and self._board[row - 4][column - 4] is None):
                    return True
                # Up-right double
                elif (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                      white_list and self._board[row - 3][column + 3] is None):
                    return True
                # Up-left
                if self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 6:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] in
                      white_list and self._board[row - 4][column - 4] is None):
                    return True
                elif (self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] in
                      white_list and self._board[row - 5][column - 5] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in white_list and self._board[row - 5][column - 5] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
            elif row == 4 and column == 1:
                # Up-right double
                if (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                        white_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] in
                      white_list and self._board[row - 4][column + 4] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                      white_list and self._board[row + 3][column + 3] is None):
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 4 and column == 3:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                # Up-right double
                elif (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                      white_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] in
                      white_list and self._board[row - 4][column + 4] is None):
                    return True
                # Down-left double
                elif (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                      white_list and self._board[row + 3][column - 3] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                      white_list and self._board[row + 3][column + 3] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in white_list and self._board[row - 4][column + 4] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 4 and column == 5:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] in
                      white_list and self._board[row - 4][column - 4] is None):
                    return True
                # Down-left double
                elif (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                      white_list and self._board[row + 3][column - 3] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 4 and column == 7:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] in
                      white_list and self._board[row - 4][column - 4] is None):
                    return True
                # Down-left
                elif (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                      white_list and self._board[row + 3][column - 3] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in white_list and self._board[row - 4][column - 4] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
            elif row == 3 and column == 0:
                # Up-right double
                if (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                        white_list and self._board[row - 3][column + 3] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                      white_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] in
                      white_list and self._board[row + 4][column + 4] is None):
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 3 and column == 2:
                # Up-right double
                if (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                        white_list and self._board[row - 3][column + 3] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                      white_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] in
                      white_list and self._board[row + 4][column + 4] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 3 and column == 4:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                # Up-right double
                elif (self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] in
                      white_list and self._board[row - 3][column + 3] is None):
                    return True
                # Down-left double
                elif (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                      white_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] in
                      white_list and self._board[row + 4][column - 4] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                      white_list and self._board[row + 3][column + 3] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in white_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 3 and column == 6:
                # Up-left double
                if (self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] in
                        white_list and self._board[row - 3][column - 3] is None):
                    return True
                # Down-left double
                elif (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                      white_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] in
                      white_list and self._board[row + 4][column - 4] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in white_list and self._board[row - 3][column - 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
            elif row == 2 and column == 1:
                # Down-right double
                if (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                        white_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] in
                      white_list and self._board[row + 4][column + 4] is None):
                    return True
                elif (self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] in
                      white_list and self._board[row + 5][column + 5] is None):
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in white_list and self._board[row + 5][column + 5] is None:
                    return True
            elif row == 2 and column == 3:
                # Down-left double
                if (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                        white_list and self._board[row + 3][column - 3] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                      white_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] in
                      white_list and self._board[row + 4][column + 4] is None):
                    return True
                    # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 2 and column == 5:
                # Down-left double
                if (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                        white_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] in
                      white_list and self._board[row + 4][column - 4] is None):
                    return True
                elif (self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] in
                      white_list and self._board[row + 5][column - 5] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in white_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 2 and column == 7:
                # Down-left double
                if (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                        white_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] in
                      white_list and self._board[row + 4][column - 4] is None):
                    return True
                elif (self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] in
                      white_list and self._board[row + 5][column - 5] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in white_list and self._board[row - 2][column - 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] is None:
                    return True
            elif row == 1 and column == 0:
                # Down-right double
                if (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                        white_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] in
                      white_list and self._board[row + 4][column + 4] is None):
                    return True
                elif (self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] in
                      white_list and self._board[row + 5][column + 5] is None):
                    return True
                elif (self._board[row + 4][column + 4] in white_list and self._board[row + 5][column + 5] in
                      white_list and self._board[row + 6][column + 6] is None):
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in white_list and self._board[row + 5][column + 5] is None:
                    return True
                elif self._board[row + 5][column + 5] in white_list and self._board[row + 6][column + 6] is None:
                    return True
            elif row == 1 and column == 2:
                # Down-right double
                if (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                        white_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] in
                      white_list and self._board[row + 4][column + 4] is None):
                    return True
                elif (self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] in
                      white_list and self._board[row + 5][column + 5] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in white_list and self._board[row + 5][column + 5] is None:
                    return True
            elif row == 1 and column == 4:
                # Down-left double
                if (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                        white_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] in
                      white_list and self._board[row + 4][column - 4] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                      white_list and self._board[row + 3][column + 3] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 1 and column == 6:
                # Down-left double
                if (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                        white_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] in
                      white_list and self._board[row + 4][column - 4] is None):
                    return True
                elif (self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] in
                      white_list and self._board[row + 5][column - 5] is None):
                    return True
                elif (self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] in
                      white_list and self._board[row + 6][column - 6] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] is None:
                    return True
                elif self._board[row + 5][column - 5] in white_list and self._board[row + 6][column - 6] is None:
                    return True
            elif row == 0 and column == 1:
                # Down-right double
                if (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                        white_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] in
                      white_list and self._board[row + 4][column + 4] is None):
                    return True
                elif (self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] in
                      white_list and self._board[row + 5][column + 5] is None):
                    return True
                elif (self._board[row + 4][column + 4] in white_list and self._board[row + 5][column + 5] in
                      white_list and self._board[row + 6][column + 6] is None):
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in white_list and self._board[row + 5][column + 5] is None:
                    return True
                elif self._board[row + 5][column + 5] in white_list and self._board[row + 6][column + 6] is None:
                    return True
            elif row == 0 and column == 3:
                # Down-left double
                if (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                        white_list and self._board[row + 3][column - 3] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] in
                      white_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] in
                      white_list and self._board[row + 4][column + 4] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in white_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in white_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 0 and column == 5:
                # Down-left double
                if (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                        white_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] in
                      white_list and self._board[row + 4][column - 4] is None):
                    return True
                elif (self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] in
                      white_list and self._board[row + 5][column - 5] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in white_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 0 and column == 7:
                # Down-left double
                if (self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] in
                        white_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] in
                      white_list and self._board[row + 4][column - 4] is None):
                    return True
                elif (self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] in
                      white_list and self._board[row + 5][column - 5] is None):
                    return True
                elif (self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] in
                      white_list and self._board[row + 6][column - 6] is None):
                    return True
                elif (self._board[row + 5][column - 5] in white_list and self._board[row + 6][column - 6] in
                      white_list and self._board[row + 7][column - 7] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in white_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in white_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in white_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in white_list and self._board[row + 5][column - 5] is None:
                    return True
                elif self._board[row + 5][column - 5] in white_list and self._board[row + 6][column - 6] is None:
                    return True
                elif self._board[row + 6][column - 6] in white_list and self._board[row + 7][column - 7] is None:
                    return True
        # White Kings' Capture Logic
        elif start == "White_king":
            if row == 7 and column == 0:
                # Up-right
                if self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] is None:
                    return True
                elif self._board[row - 5][column + 5] in black_list and self._board[row - 6][column + 6] is None:
                    return True
                elif self._board[row - 6][column + 6] in black_list and self._board[row - 7][column + 7] is None:
                    return True
            elif row == 7 and column == 2:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] is None:
                    return True
            elif row == 7 and column == 4:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
            elif row == 7 and column == 6:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in black_list and self._board[row - 5][column - 5] is None:
                    return True
                elif self._board[row - 5][column - 5] in black_list and self._board[row - 6][column - 6] is None:
                    return True
            elif row == 6 and column == 1:
                # Up-right
                if self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] is None:
                    return True
                elif self._board[row - 5][column + 5] in black_list and self._board[row - 6][column + 6] is None:
                    return True
            elif row == 6 and column == 3:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
            elif row == 6 and column == 5:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in black_list and self._board[row - 5][column - 5] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
            elif row == 6 and column == 7:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in black_list and self._board[row - 5][column - 5] is None:
                    return True
                elif self._board[row - 5][column - 5] in black_list and self._board[row - 6][column - 6] is None:
                    return True
            elif row == 5 and column == 0:
                # Up-right
                if self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] is None:
                    return True
                # down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 2:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 4:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 4][column - 4] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 6:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in black_list and self._board[row - 5][column - 5] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
            elif row == 4 and column == 1:
                # Up-right
                if self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 4 and column == 3:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 4 and column == 5:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 4 and column == 7:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
            elif row == 3 and column == 0:
                # Up-right
                if self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 3 and column == 2:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 3 and column == 4:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 3 and column == 6:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
            elif row == 2 and column == 1:
                # Up-right
                if self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in black_list and self._board[row + 5][column + 5] is None:
                    return True
            elif row == 2 and column == 3:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 2 and column == 5:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 2 and column == 7:
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] is None:
                    return True
            elif row == 1 and column == 0:
                # Down-right
                if self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in black_list and self._board[row + 5][column + 5] is None:
                    return True
                elif self._board[row + 5][column + 5] in black_list and self._board[row + 6][column + 6] is None:
                    return True
            elif row == 1 and column == 2:
                # Down-left
                if self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in black_list and self._board[row + 5][column + 5] is None:
                    return True
            elif row == 1 and column == 4:
                # Down-left
                if self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 1 and column == 6:
                # Down-left
                if self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] is None:
                    return True
                elif self._board[row + 5][column - 5] in black_list and self._board[row + 6][column - 6] is None:
                    return True
            elif row == 0 and column == 1:
                # Down-right
                if self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in black_list and self._board[row + 5][column + 5] is None:
                    return True
                elif self._board[row + 5][column + 5] in black_list and self._board[row + 6][column + 6] is None:
                    return True
            elif row == 0 and column == 3:
                # Down-left
                if self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 0 and column == 5:
                # Down-left
                if self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 0 and column == 7:
                # Down-left
                if self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] is None:
                    return True
                elif self._board[row + 5][column - 5] in black_list and self._board[row + 6][column - 6] is None:
                    return True
                elif self._board[row + 6][column - 6] in black_list and self._board[row + 7][column - 7] is None:
                    return True
        elif start == "White_Triple_King":
            if row == 7 and column == 0:
                # Up-right double
                if (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                        black_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] in
                      black_list and self._board[row - 4][column + 4] is None):
                    return True
                elif (self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] in
                      black_list and self._board[row - 5][column + 5] is None):
                    return True
                elif (self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] in
                      black_list and self._board[row - 6][column + 6] is None):
                    return True
                elif (self._board[row - 5][column + 5] in black_list and self._board[row - 6][column + 6] in
                      black_list and self._board[row - 7][column + 7]) is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] is None:
                    return True
                elif self._board[row - 5][column + 5] in black_list and self._board[row - 6][column + 6] is None:
                    return True
                elif self._board[row - 6][column + 6] in black_list and self._board[row - 7][column + 7] is None:
                    return True
            elif row == 7 and column == 2:
                # Up-right double
                if (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                        black_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] in
                      black_list and self._board[row - 4][column + 4] is None):
                    return True
                elif (self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] in
                      black_list and self._board[row - 5][column + 5] is None):
                    return True
                elif (self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] in
                      black_list and self._board[row - 6][column + 6] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] is None:
                    return True
            elif row == 7 and column == 4:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] in
                      black_list and self._board[row - 4][column - 4] is None):
                    return True
                # Up-right double
                elif (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                      black_list and self._board[row - 3][column + 3] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
            elif row == 7 and column == 6:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] in
                      black_list and self._board[row - 4][column - 4] is None):
                    return True
                elif (self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] in
                      black_list and self._board[row - 5][column - 5] is None):
                    return True
                elif (self._board[row - 4][column - 4] in black_list and self._board[row - 5][column - 5] in
                      black_list and self._board[row - 6][column - 6] is None):
                    return True
                    # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in black_list and self._board[row - 5][column - 5] is None:
                    return True
                elif self._board[row - 5][column - 5] in black_list and self._board[row - 6][column - 6] is None:
                    return True
            elif row == 6 and column == 1:
                # Up-right double
                if (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                        black_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] in
                      black_list and self._board[row - 4][column + 4] is None):
                    return True
                elif (self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] in
                      black_list and self._board[row - 5][column + 5] is None):
                    return True
                elif (self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] in
                      black_list and self._board[row - 6][column + 6] is None):
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] is None:
                    return True
                elif self._board[row - 5][column + 5] in black_list and self._board[row - 6][column + 6] is None:
                    return True
            elif row == 6 and column == 3:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                # Up-right double
                elif (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                      black_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] in
                      black_list and self._board[row - 4][column + 4] is None):
                    return True
            elif row == 6 and column == 5:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] in
                      black_list and self._board[row - 4][column - 4] is None):
                    return True
                elif (self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] in
                      black_list and self._board[row - 5][column - 5] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in black_list and self._board[row - 5][column - 5] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
            elif row == 6 and column == 7:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] in
                      black_list and self._board[row - 4][column - 4] is None):
                    return True
                elif (self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] in
                      black_list and self._board[row - 5][column - 5] is None):
                    return True
                elif (self._board[row - 4][column - 4] in black_list and self._board[row - 5][column - 5] in
                      black_list and self._board[row - 6][column - 6] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in black_list and self._board[row - 5][column - 5] is None:
                    return True
                elif self._board[row - 5][column - 5] in black_list and self._board[row - 6][column - 6] is None:
                    return True
            elif row == 5 and column == 0:
                # Up-right double
                if (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                        black_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] in
                      black_list and self._board[row - 4][column + 4] is None):
                    return True
                elif (self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] in
                      black_list and self._board[row - 5][column + 5] is None):
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 2:
                # Up-right double
                if (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                        black_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] in
                      black_list and self._board[row - 4][column + 4] is None):
                    return True
                elif (self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] in
                      black_list and self._board[row - 5][column + 5] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                elif self._board[row - 4][column + 4] in black_list and self._board[row - 5][column + 5] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 4:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] in
                      black_list and self._board[row - 4][column - 4] is None):
                    return True
                # Up-right double
                elif (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                      black_list and self._board[row - 3][column + 3] is None):
                    return True
                # Up-left
                if self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 5 and column == 6:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] in
                      black_list and self._board[row - 4][column - 4] is None):
                    return True
                elif (self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] in
                      black_list and self._board[row - 5][column - 5] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                elif self._board[row - 4][column - 4] in black_list and self._board[row - 5][column - 5] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
            elif row == 4 and column == 1:
                # Up-right double
                if (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                        black_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] in
                      black_list and self._board[row - 4][column + 4] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                      black_list and self._board[row + 3][column + 3] is None):
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 4 and column == 3:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                # Up-right double
                elif (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                      black_list and self._board[row - 3][column + 3] is None):
                    return True
                elif (self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] in
                      black_list and self._board[row - 4][column + 4] is None):
                    return True
                # Down-left double
                elif (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                      black_list and self._board[row + 3][column - 3] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                      black_list and self._board[row + 3][column + 3] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                elif self._board[row - 3][column + 3] in black_list and self._board[row - 4][column + 4] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 4 and column == 5:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] in
                      black_list and self._board[row - 4][column - 4] is None):
                    return True
                # Down-left double
                elif (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                      black_list and self._board[row + 3][column - 3] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 4 and column == 7:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                elif (self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] in
                      black_list and self._board[row - 4][column - 4] is None):
                    return True
                # Down-left
                elif (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                      black_list and self._board[row + 3][column - 3] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                elif self._board[row - 3][column - 3] in black_list and self._board[row - 4][column - 4] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
            elif row == 3 and column == 0:
                # Up-right double
                if (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                        black_list and self._board[row - 3][column + 3] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                      black_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] in
                      black_list and self._board[row + 4][column + 4] is None):
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 3 and column == 2:
                # Up-right double
                if (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                        black_list and self._board[row - 3][column + 3] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                      black_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] in
                      black_list and self._board[row + 4][column + 4] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 3 and column == 4:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                # Up-right double
                elif (self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] in
                      black_list and self._board[row - 3][column + 3] is None):
                    return True
                # Down-left double
                elif (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                      black_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] in
                      black_list and self._board[row + 4][column - 4] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                      black_list and self._board[row + 3][column + 3] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                elif self._board[row - 2][column + 2] in black_list and self._board[row - 3][column + 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 3 and column == 6:
                # Up-left double
                if (self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] in
                        black_list and self._board[row - 3][column - 3] is None):
                    return True
                # Down-left double
                elif (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                      black_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] in
                      black_list and self._board[row + 4][column - 4] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                elif self._board[row - 2][column - 2] in black_list and self._board[row - 3][column - 3] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
            elif row == 2 and column == 1:
                # Down-right double
                if (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                        black_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] in
                      black_list and self._board[row + 4][column + 4] is None):
                    return True
                elif (self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] in
                      black_list and self._board[row + 5][column + 5] is None):
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in black_list and self._board[row + 5][column + 5] is None:
                    return True
            elif row == 2 and column == 3:
                # Down-left double
                if (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                        black_list and self._board[row + 3][column - 3] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                      black_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] in
                      black_list and self._board[row + 4][column + 4] is None):
                    return True
                    # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 2 and column == 5:
                # Down-left double
                if (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                        black_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] in
                      black_list and self._board[row + 4][column - 4] is None):
                    return True
                elif (self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] in
                      black_list and self._board[row + 5][column - 5] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Up-right
                elif self._board[row - 1][column + 1] in black_list and self._board[row - 2][column + 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 2 and column == 7:
                # Down-left double
                if (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                        black_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] in
                      black_list and self._board[row + 4][column - 4] is None):
                    return True
                elif (self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] in
                      black_list and self._board[row + 5][column - 5] is None):
                    return True
                # Up-left
                elif self._board[row - 1][column - 1] in black_list and self._board[row - 2][column - 2] is None:
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] is None:
                    return True
            elif row == 1 and column == 0:
                # Down-right double
                if (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                        black_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] in
                      black_list and self._board[row + 4][column + 4] is None):
                    return True
                elif (self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] in
                      black_list and self._board[row + 5][column + 5] is None):
                    return True
                elif (self._board[row + 4][column + 4] in black_list and self._board[row + 5][column + 5] in
                      black_list and self._board[row + 6][column + 6] is None):
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in black_list and self._board[row + 5][column + 5] is None:
                    return True
                elif self._board[row + 5][column + 5] in black_list and self._board[row + 6][column + 6] is None:
                    return True
            elif row == 1 and column == 2:
                # Down-right double
                if (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                        black_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] in
                      black_list and self._board[row + 4][column + 4] is None):
                    return True
                elif (self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] in
                      black_list and self._board[row + 5][column + 5] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in black_list and self._board[row + 5][column + 5] is None:
                    return True
            elif row == 1 and column == 4:
                # Down-left double
                if (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                        black_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] in
                      black_list and self._board[row + 4][column - 4] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                      black_list and self._board[row + 3][column + 3] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
            elif row == 1 and column == 6:
                # Down-left double
                if (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                        black_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] in
                      black_list and self._board[row + 4][column - 4] is None):
                    return True
                elif (self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] in
                      black_list and self._board[row + 5][column - 5] is None):
                    return True
                elif (self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] in
                      black_list and self._board[row + 6][column - 6] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] is None:
                    return True
                elif self._board[row + 5][column - 5] in black_list and self._board[row + 6][column - 6] is None:
                    return True
            elif row == 0 and column == 1:
                # Down-right double
                if (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                        black_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] in
                      black_list and self._board[row + 4][column + 4] is None):
                    return True
                elif (self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] in
                      black_list and self._board[row + 5][column + 5] is None):
                    return True
                elif (self._board[row + 4][column + 4] in black_list and self._board[row + 5][column + 5] in
                      black_list and self._board[row + 6][column + 6] is None):
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
                elif self._board[row + 4][column + 4] in black_list and self._board[row + 5][column + 5] is None:
                    return True
                elif self._board[row + 5][column + 5] in black_list and self._board[row + 6][column + 6] is None:
                    return True
            elif row == 0 and column == 3:
                # Down-left double
                if (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                        black_list and self._board[row + 3][column - 3] is None):
                    return True
                # Down-right double
                elif (self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] in
                      black_list and self._board[row + 3][column + 3] is None):
                    return True
                elif (self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] in
                      black_list and self._board[row + 4][column + 4] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
                elif self._board[row + 2][column + 2] in black_list and self._board[row + 3][column + 3] is None:
                    return True
                elif self._board[row + 3][column + 3] in black_list and self._board[row + 4][column + 4] is None:
                    return True
            elif row == 0 and column == 5:
                # Down-left double
                if (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                        black_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] in
                      black_list and self._board[row + 4][column - 4] is None):
                    return True
                elif (self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] in
                      black_list and self._board[row + 5][column - 5] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] is None:
                    return True
                # Down-right
                elif self._board[row + 1][column + 1] in black_list and self._board[row + 2][column + 2] is None:
                    return True
            elif row == 0 and column == 7:
                # Down-left double
                if (self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] in
                        black_list and self._board[row + 3][column - 3] is None):
                    return True
                elif (self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] in
                      black_list and self._board[row + 4][column - 4] is None):
                    return True
                elif (self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] in
                      black_list and self._board[row + 5][column - 5] is None):
                    return True
                elif (self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] in
                      black_list and self._board[row + 6][column - 6] is None):
                    return True
                elif (self._board[row + 5][column - 5] in black_list and self._board[row + 6][column - 6] in
                      black_list and self._board[row + 7][column - 7] is None):
                    return True
                # Down-left
                elif self._board[row + 1][column - 1] in black_list and self._board[row + 2][column - 2] is None:
                    return True
                elif self._board[row + 2][column - 2] in black_list and self._board[row + 3][column - 3] is None:
                    return True
                elif self._board[row + 3][column - 3] in black_list and self._board[row + 4][column - 4] is None:
                    return True
                elif self._board[row + 4][column - 4] in black_list and self._board[row + 5][column - 5] is None:
                    return True
                elif self._board[row + 5][column - 5] in black_list and self._board[row + 6][column - 6] is None:
                    return True
                elif self._board[row + 6][column - 6] in black_list and self._board[row + 7][column - 7] is None:
                    return True
        else:
            return False

    def make_move(self, player_name, starting_square_location, destination_square_location):
        """
        Class method that takes three parameters:
        player_name                  = string containing the moving player's name.
        starting_square_location     = tuple in (x,y) format representing the starting square a piece is moving from
        destination_square_location  = tuple in (x,y) format representing the square a piece is moving to

        This method evaluates a piece starting location by calling class method 'can_capture' to determine if a piece
        can capture. If true, the board is changed to reflect the move, including removing the capture piece(s) and
        updating the data members of the Player objects. If false, simple non-capture movement is made e.x. moving a
        pawn onto an empty space. The board is changed to reflect the move.
        """

        starting_row, starting_column = starting_square_location[0], starting_square_location[1]
        destination_row, destination_column = destination_square_location[0], destination_square_location[1]
        start, player_one, player_two = self.get_checker_details(starting_square_location), None, None
        white_list, black_list = ["White", "White_king", "White_Triple_King"], ["Black", "Black_king",
                                                                                "Black_Triple_King"]

        for players in self._players:
            player_object = self._players[players]
            if player_object.get_checker_color() == "Black":
                player_one = player_object
            else:
                player_two = player_object

        if self.can_capture(starting_square_location) is True:
            self._capture_state = True
        else:
            self._capture_state = False

        # Basic non capture movement for all pieces
        if self._capture_state is False:
            if start == "Black":
                self._board[starting_row][starting_column] = None
                self._board[destination_row][destination_column] = "Black"
            elif start == "Black_king":
                self._board[starting_row][starting_column] = None
                self._board[destination_row][destination_column] = "Black_king"
            elif start == "Black_Triple_King":
                self._board[starting_row][starting_column] = None
                self._board[destination_row][destination_column] = "Black_Triple_King"
            elif start == "White":
                self._board[starting_row][starting_column] = None
                self._board[destination_row][destination_column] = "White"
            elif start == "White_king":
                self._board[starting_row][starting_column] = None
                self._board[destination_row][destination_column] = "White_king"
            elif start == "White_Triple_King":
                self._board[starting_row][starting_column] = None
                self._board[destination_row][destination_column] = "White_Triple_King"

        # Capture movement
        if self._capture_state is True:
            # Capture logic for Black Pawn
            if start == "Black":
                self._players[player_name].add_captured_pieces()
                self._board[starting_row][starting_column] = None
                self._board[destination_row][destination_column] = "Black"
                if starting_row != 1 and starting_column == 0:
                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                elif starting_column == 7:
                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                elif starting_column == 1:
                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                elif starting_row != 1 and starting_column == 6:
                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                elif starting_row != 1:
                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
            # Capture logic for White Pawn
            elif start == "White":
                self._players[player_name].add_captured_pieces()
                self._board[starting_row][starting_column] = None
                self._board[destination_row][destination_column] = "White"
                if starting_row != 6 and starting_column == 7:
                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                elif starting_column == 0:
                    # Capture down-right
                    if self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row != 6 and starting_column == 1:
                    # Capture down-right
                    if self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_column == 6:
                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                elif starting_row != 6:
                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
            # Capture logic for Black Kings
            elif start == "Black_king" or start == "Black_Triple_King":
                self._board[starting_row][starting_column] = None
                self._players[player_name].add_captured_pieces()
                if start == "Black_king":
                    self._board[destination_row][destination_column] = "Black_king"
                if start == "Black_Triple_King":
                    self._board[destination_row][destination_column] = "Black_Triple_King"
                if starting_row == 7 and starting_column == 0:
                    if start == "Black_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] in white_list and \
                                self._board[starting_row - 5][starting_column + 5] is not None:
                            if self._board[starting_row - 3][starting_column + 3] == "White_king" or \
                                    self._board[starting_row - 4][starting_column + 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 3][starting_column + 3] == "White_Triple_King" or \
                                    self._board[starting_row - 4][starting_column + 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 4][starting_column + 4] in white_list and \
                                self._board[starting_row - 5][starting_column + 5] in white_list and \
                                self._board[starting_row - 6][starting_column + 6] is not None:
                            if self._board[starting_row - 4][starting_column + 4] == "White_king" or \
                                    self._board[starting_row - 5][starting_column + 5] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 4][starting_column + 4] == "White_Triple_King" or \
                                    self._board[starting_row - 5][starting_column + 5] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._board[starting_row - 5][starting_column + 5] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 5][starting_column + 5] in white_list and \
                                self._board[starting_row - 6][starting_column + 6] in white_list and \
                                self._board[starting_row - 7][starting_column + 7] is not None:
                            if self._board[starting_row - 5][starting_column + 5] == "White_king" or \
                                    self._board[starting_row - 6][starting_column + 6] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 5][starting_column + 5] == "White_Triple_King" or \
                                    self._board[starting_row - 6][starting_column + 6] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 5][starting_column + 5] = None
                            self._board[starting_row - 6][starting_column + 6] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    elif self._board[starting_row - 4][starting_column + 4] in white_list and \
                            self._board[starting_row - 5][starting_column + 5] is not None:
                        if self._board[starting_row - 4][starting_column + 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 4][starting_column + 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 4][starting_column + 4] = None
                    elif self._board[starting_row - 5][starting_column + 5] in white_list and \
                            self._board[starting_row - 6][starting_column + 6] is not None:
                        if self._board[starting_row - 5][starting_column + 5] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 5][starting_column + 5] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 5][starting_column + 5] = None
                    elif self._board[starting_row - 6][starting_column + 6] in white_list and \
                            self._board[starting_row - 7][starting_column + 7] is not None:
                        if self._board[starting_row - 6][starting_column + 6] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 6][starting_column + 6] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 6][starting_column + 6] = None
                elif starting_row == 7 and starting_column == 2:
                    if start == "Black_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] in white_list and \
                                self._board[starting_row - 5][starting_column + 5] is not None:
                            if self._board[starting_row - 3][starting_column + 3] == "White_king" or \
                                    self._board[starting_row - 4][starting_column + 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 3][starting_column + 3] == "White_Triple_King" or \
                                    self._board[starting_row - 4][starting_column + 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 4][starting_column + 4] in white_list and \
                                self._board[starting_row - 5][starting_column + 5] in white_list and \
                                self._board[starting_row - 6][starting_column + 6] is not None:
                            if self._board[starting_row - 4][starting_column + 4] == "White_king" or \
                                    self._board[starting_row - 5][starting_column + 5] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 4][starting_column + 4] == "White_Triple_King" or \
                                    self._board[starting_row - 5][starting_column + 5] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._board[starting_row - 5][starting_column + 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    elif self._board[starting_row - 4][starting_column + 4] in white_list and \
                            self._board[starting_row - 5][starting_column + 5] is not None:
                        if self._board[starting_row - 4][starting_column + 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 4][starting_column + 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 4][starting_column + 4] = None
                elif starting_row == 7 and starting_column == 4:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture up-right double
                        elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                elif starting_row == 7 and starting_column == 6:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] in white_list and \
                                self._board[starting_row - 5][starting_column - 5] is not None:
                            if self._board[starting_row - 3][starting_column - 3] == "White_king" or \
                                    self._board[starting_row - 4][starting_column - 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 3][starting_column - 3] == "White_Triple_King" or \
                                    self._board[starting_row - 4][starting_column - 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._board[starting_row - 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 4][starting_column - 4] in white_list and \
                                self._board[starting_row - 5][starting_column - 5] in white_list and \
                                self._board[starting_row - 6][starting_column - 6] is not None:
                            if self._board[starting_row - 4][starting_column - 4] == "White_king" or \
                                    self._board[starting_row - 5][starting_column - 5] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 4][starting_column - 4] == "White_Triple_King" or \
                                    self._board[starting_row - 5][starting_column - 5] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 4][starting_column - 4] = None
                            self._board[starting_row - 5][starting_column - 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    elif self._board[starting_row - 4][starting_column - 4] in white_list and \
                            self._board[starting_row - 5][starting_column - 5] is not None:
                        if self._board[starting_row - 4][starting_column - 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 4][starting_column - 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 4][starting_column - 4] = None
                    elif self._board[starting_row - 5][starting_column - 5] in white_list and \
                            self._board[starting_row - 6][starting_column - 6] is not None:
                        if self._board[starting_row - 5][starting_column - 5] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 5][starting_column - 5] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 5][starting_column - 5] = None
                elif starting_row == 6 and starting_column == 1:
                    if start == "Black_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] in white_list and \
                                self._board[starting_row - 5][starting_column + 5] is not None:
                            if self._board[starting_row - 3][starting_column + 3] == "White_king" or \
                                    self._board[starting_row - 4][starting_column + 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 3][starting_column + 3] == "White_Triple_King" or \
                                    self._board[starting_row - 4][starting_column + 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 4][starting_column + 4] in white_list and \
                                self._board[starting_row - 5][starting_column + 5] in white_list and \
                                self._board[starting_row - 6][starting_column + 6] is not None:
                            if self._board[starting_row - 4][starting_column + 4] == "White_king" or \
                                    self._board[starting_row - 5][starting_column + 5] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 4][starting_column + 4] == "White_Triple_King" or \
                                    self._board[starting_row - 5][starting_column + 5] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._board[starting_row - 5][starting_column + 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    elif self._board[starting_row - 4][starting_column + 4] in white_list and \
                            self._board[starting_row - 5][starting_column + 5] is not None:
                        if self._board[starting_row - 4][starting_column + 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 4][starting_column + 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 4][starting_column + 4] = None
                    elif self._board[starting_row - 5][starting_column + 5] in white_list and \
                            self._board[starting_row - 6][starting_column + 6] is not None:
                        if self._board[starting_row - 5][starting_column + 5] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 5][starting_column + 5] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 5][starting_column + 5] = None
                elif starting_row == 6 and starting_column == 3:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture up-right double
                        elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                elif starting_row == 6 and starting_column == 5:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] in white_list and \
                                self._board[starting_row - 5][starting_column - 5] is not None:
                            if self._board[starting_row - 3][starting_column - 3] == "White_king" or \
                                    self._board[starting_row - 4][starting_column - 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 3][starting_column - 3] == "White_Triple_King" or \
                                    self._board[starting_row - 4][starting_column - 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._board[starting_row - 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                if self._board[starting_row - 1][starting_column - 1] in white_list and \
                        self._board[starting_row - 2][starting_column - 2] is not None:
                    if self._board[starting_row - 1][starting_column - 1] == "White_king":
                        player_two.remove_king()
                    elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                        player_two.remove_triple_king()
                    self._board[starting_row - 1][starting_column - 1] = None
                elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                        self._board[starting_row - 3][starting_column - 3] is not None:
                    if self._board[starting_row - 2][starting_column - 2] == "White_king":
                        player_two.remove_king()
                    elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                        player_two.remove_triple_king()
                    self._board[starting_row - 2][starting_column - 2] = None
                elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                        self._board[starting_row - 4][starting_column - 4] is not None:
                    if self._board[starting_row - 3][starting_column - 3] == "White_king":
                        player_two.remove_king()
                    elif self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                        player_two.remove_triple_king()
                    self._board[starting_row - 3][starting_column - 3] = None
                elif self._board[starting_row - 4][starting_column - 4] in white_list and \
                        self._board[starting_row - 5][starting_column - 5] is not None:
                    if self._board[starting_row - 4][starting_column - 4] == "White_king":
                        player_two.remove_king()
                    elif self._board[starting_row - 4][starting_column - 4] == "White_Triple_King":
                        player_two.remove_triple_king()
                    self._board[starting_row - 4][starting_column - 4] = None
                    # Capture up-right
                elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                        self._board[starting_row - 2][starting_column + 2] is not None:
                    if self._board[starting_row - 1][starting_column + 1] == "White_king":
                        player_two.remove_king()
                    elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                        player_two.remove_triple_king()
                    self._board[starting_row - 1][starting_column + 1] = None
                elif starting_row == 6 and starting_column == 7:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] in white_list and \
                                self._board[starting_row - 5][starting_column - 5] is not None:
                            if self._board[starting_row - 3][starting_column - 3] == "White_king" or \
                                    self._board[starting_row - 4][starting_column - 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 3][starting_column - 3] == "White_Triple_King" or \
                                    self._board[starting_row - 4][starting_column - 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._board[starting_row - 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 4][starting_column - 4] in white_list and \
                                self._board[starting_row - 5][starting_column - 5] in white_list and \
                                self._board[starting_row - 6][starting_column - 6] is not None:
                            if self._board[starting_row - 4][starting_column - 4] == "White_king" or \
                                    self._board[starting_row - 5][starting_column - 5] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 4][starting_column - 4] == "White_Triple_King" or \
                                    self._board[starting_row - 5][starting_column - 5] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 4][starting_column - 4] = None
                            self._board[starting_row - 5][starting_column - 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    elif self._board[starting_row - 4][starting_column - 4] in white_list and \
                            self._board[starting_row - 5][starting_column - 5] is not None:
                        if self._board[starting_row - 4][starting_column - 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 4][starting_column - 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 4][starting_column - 4] = None
                    elif self._board[starting_row - 5][starting_column - 5] in white_list and \
                            self._board[starting_row - 6][starting_column - 6] is not None:
                        if self._board[starting_row - 5][starting_column - 5] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 5][starting_column - 5] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 5][starting_column - 5] = None
                elif starting_row == 5 and starting_column == 0:
                    if start == "Black_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] in white_list and \
                                self._board[starting_row - 5][starting_column + 5] is not None:
                            if self._board[starting_row - 3][starting_column + 3] == "White_king" or \
                                    self._board[starting_row - 4][starting_column + 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 3][starting_column + 3] == "White_Triple_King" or \
                                    self._board[starting_row - 4][starting_column + 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    elif self._board[starting_row - 4][starting_column + 4] in white_list and \
                            self._board[starting_row - 5][starting_column + 5] is not None:
                        if self._board[starting_row - 4][starting_column + 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 4][starting_column + 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 4][starting_column + 4] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 5 and starting_column == 2:
                    if start == "Black_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] in white_list and \
                                self._board[starting_row - 5][starting_column + 5] is not None:
                            if self._board[starting_row - 3][starting_column + 3] == "White_king" or \
                                    self._board[starting_row - 4][starting_column + 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 3][starting_column + 3] == "White_Triple_King" or \
                                    self._board[starting_row - 4][starting_column + 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    elif self._board[starting_row - 4][starting_column + 4] in white_list and \
                            self._board[starting_row - 5][starting_column + 5] is not None:
                        if self._board[starting_row - 4][starting_column + 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 4][starting_column + 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 4][starting_column + 4] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 5 and starting_column == 4:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture up-right double
                        elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                        # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                        # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 5 and starting_column == 6:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] in white_list and \
                                self._board[starting_row - 5][starting_column - 5] is not None:
                            if self._board[starting_row - 3][starting_column - 3] == "White_king" or \
                                    self._board[starting_row - 4][starting_column - 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 3][starting_column - 3] == "White_Triple_King" or \
                                    self._board[starting_row - 4][starting_column - 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                                self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    elif self._board[starting_row - 4][starting_column - 4] in white_list and \
                            self._board[starting_row - 5][starting_column - 5] is not None:
                        if self._board[starting_row - 4][starting_column - 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 4][starting_column - 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 4][starting_column - 4] = None
                    elif self._board[starting_row - 5][starting_column - 5] in white_list and \
                            self._board[starting_row - 6][starting_column - 6] is not None:
                        if self._board[starting_row - 5][starting_column - 5] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 5][starting_column - 5] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 5][starting_column - 5] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                elif starting_row == 4 and starting_column == 1:
                    if start == "Black_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                elif starting_row == 4 and starting_column == 3:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture up-right double
                        elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] in white_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-left double
                        elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in white_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                elif starting_row == 4 and starting_column == 5:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-left double
                        elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                        # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 4 and starting_column == 7:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] in white_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-left double
                        elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in white_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                elif starting_row == 3 and starting_column == 0:
                    if start == "Black_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                elif starting_row == 3 and starting_column == 2:
                    if start == "Black_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                elif starting_row == 3 and starting_column == 4:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture up-right double
                        elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                                self._board[starting_row - 2][starting_column + 2] in white_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-left double
                        elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in white_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                elif starting_row == 3 and starting_column == 6:
                    if start == "Black_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in white_list and \
                                self._board[starting_row - 2][starting_column - 2] in white_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-left double
                        elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in white_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                elif starting_row == 2 and starting_column == 1:
                    if start == "Black_Triple_King":
                        # Capture down-right double
                        if self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] in white_list and \
                                self._board[starting_row + 5][starting_column + 5] is not None:
                            if self._board[starting_row + 3][starting_column + 3] == "White_king" or \
                                    self._board[starting_row + 4][starting_column + 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 3][starting_column + 3] == "White_Triple_King" or \
                                    self._board[starting_row + 4][starting_column + 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                    elif self._board[starting_row + 4][starting_column + 4] in white_list and \
                            self._board[starting_row + 5][starting_column + 5] is not None:
                        if self._board[starting_row + 4][starting_column + 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 4][starting_column + 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 4][starting_column + 4] = None
                elif starting_row == 2 and starting_column == 3:
                    if start == "Black_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                elif starting_row == 2 and starting_column == 5:
                    if start == "Black_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] in white_list and \
                                self._board[starting_row + 5][starting_column - 5] is not None:
                            if self._board[starting_row + 3][starting_column - 3] == "White_king" or \
                                    self._board[starting_row + 4][starting_column - 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 3][starting_column - 3] == "White_Triple_King" or \
                                    self._board[starting_row + 4][starting_column - 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in white_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    elif self._board[starting_row + 4][starting_column - 4] in white_list and \
                            self._board[starting_row + 5][starting_column - 5] is not None:
                        if self._board[starting_row + 4][starting_column - 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 4][starting_column - 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 4][starting_column - 4] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 2 and starting_column == 7:
                    if start == "Black_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] in white_list and \
                                self._board[starting_row + 5][starting_column - 5] is not None:
                            if self._board[starting_row + 3][starting_column - 3] == "White_king" or \
                                    self._board[starting_row + 4][starting_column - 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 3][starting_column - 3] == "White_Triple_King" or \
                                    self._board[starting_row + 4][starting_column - 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in white_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    elif self._board[starting_row + 4][starting_column - 4] in white_list and \
                            self._board[starting_row + 5][starting_column - 5] is not None:
                        if self._board[starting_row + 4][starting_column - 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 4][starting_column - 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 4][starting_column - 4] = None
                elif starting_row == 1 and starting_column == 0:
                    if start == "Black_Triple_King":
                        # Capture down-right double
                        if self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] in white_list and \
                                self._board[starting_row + 5][starting_column + 5] is not None:
                            if self._board[starting_row + 3][starting_column + 3] == "White_king" or \
                                    self._board[starting_row + 4][starting_column + 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 3][starting_column + 3] == "White_Triple_King" or \
                                    self._board[starting_row + 4][starting_column + 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 4][starting_column + 4] in white_list and \
                                self._board[starting_row + 5][starting_column + 5] in white_list and \
                                self._board[starting_row + 6][starting_column + 6] is not None:
                            if self._board[starting_row + 4][starting_column + 4] == "White_king" or \
                                    self._board[starting_row + 5][starting_column + 5] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 4][starting_column + 4] == "White_Triple_King" or \
                                    self._board[starting_row + 5][starting_column + 5] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._board[starting_row + 5][starting_column + 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-right
                    if self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                    elif self._board[starting_row + 4][starting_column + 4] in white_list and \
                            self._board[starting_row + 5][starting_column + 5] is not None:
                        if self._board[starting_row + 4][starting_column + 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 4][starting_column + 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 4][starting_column + 4] = None
                    elif self._board[starting_row + 5][starting_column + 5] in white_list and \
                            self._board[starting_row + 6][starting_column + 6] is not None:
                        if self._board[starting_row + 5][starting_column + 5] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 5][starting_column + 5] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 5][starting_column + 5] = None
                elif starting_row == 1 and starting_column == 2:
                    if start == "Black_Triple_King":
                        # Capture down-right double
                        if self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] in white_list and \
                                self._board[starting_row + 5][starting_column + 5] is not None:
                            if self._board[starting_row + 3][starting_column + 3] == "White_king" or \
                                    self._board[starting_row + 4][starting_column + 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 3][starting_column + 3] == "White_Triple_King" or \
                                    self._board[starting_row + 4][starting_column + 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                    elif self._board[starting_row + 4][starting_column + 4] in white_list and \
                            self._board[starting_row + 5][starting_column + 5] is not None:
                        if self._board[starting_row + 4][starting_column + 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 4][starting_column + 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 4][starting_column + 4] = None
                elif starting_row == 1 and starting_column == 4:
                    if start == "Black_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                elif starting_row == 1 and starting_column == 6:
                    if start == "Black_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] in white_list and \
                                self._board[starting_row + 5][starting_column - 5] is not None:
                            if self._board[starting_row + 3][starting_column - 3] == "White_king" or \
                                    self._board[starting_row + 4][starting_column - 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 3][starting_column - 3] == "White_Triple_King" or \
                                    self._board[starting_row + 4][starting_column - 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 4][starting_column - 4] in white_list and \
                                self._board[starting_row + 5][starting_column - 5] in white_list and \
                                self._board[starting_row + 6][starting_column - 6] is not None:
                            if self._board[starting_row + 4][starting_column - 4] == "White_king" or \
                                    self._board[starting_row + 5][starting_column - 5] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 4][starting_column - 4] == "White_Triple_King" or \
                                    self._board[starting_row + 5][starting_column - 5] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._board[starting_row + 5][starting_column - 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    elif self._board[starting_row + 4][starting_column - 4] in white_list and \
                            self._board[starting_row + 5][starting_column - 5] is not None:
                        if self._board[starting_row + 4][starting_column - 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 4][starting_column - 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 4][starting_column - 4] = None
                    elif self._board[starting_row + 5][starting_column - 5] in white_list and \
                            self._board[starting_row + 6][starting_column - 6] is not None:
                        if self._board[starting_row + 5][starting_column - 5] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 5][starting_column - 5] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 5][starting_column - 5] = None
                elif starting_row == 0 and starting_column == 1:
                    if start == "Black_Triple_King":
                        # Capture down-right double
                        if self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] in white_list and \
                                self._board[starting_row + 5][starting_column + 5] is not None:
                            if self._board[starting_row + 3][starting_column + 3] == "White_king" or \
                                    self._board[starting_row + 4][starting_column + 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 3][starting_column + 3] == "White_Triple_King" or \
                                    self._board[starting_row + 4][starting_column + 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 4][starting_column + 4] in white_list and \
                                self._board[starting_row + 5][starting_column + 5] in white_list and \
                                self._board[starting_row + 6][starting_column + 6] is not None:
                            if self._board[starting_row + 4][starting_column + 4] == "White_king" or \
                                    self._board[starting_row + 5][starting_column + 5] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 4][starting_column + 4] == "White_Triple_King" or \
                                    self._board[starting_row + 5][starting_column + 5] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._board[starting_row + 5][starting_column + 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-right
                    if self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                    elif self._board[starting_row + 4][starting_column + 4] in white_list and \
                            self._board[starting_row + 5][starting_column + 5] is not None:
                        if self._board[starting_row + 4][starting_column + 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 4][starting_column + 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 4][starting_column + 4] = None
                    elif self._board[starting_row + 5][starting_column + 5] in white_list and \
                            self._board[starting_row + 6][starting_column + 6] is not None:
                        if self._board[starting_row + 5][starting_column + 5] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 5][starting_column + 5] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 5][starting_column + 5] = None
                elif starting_row == 0 and starting_column == 3:
                    if start == "Black_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                                self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                                self._board[starting_row + 3][starting_column + 3] in white_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in white_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in white_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                elif starting_row == 0 and starting_column == 5:
                    if start == "Black_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] in white_list and \
                                self._board[starting_row + 5][starting_column - 5] is not None:
                            if self._board[starting_row + 3][starting_column - 3] == "White_king" or \
                                    self._board[starting_row + 4][starting_column - 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 3][starting_column - 3] == "White_Triple_King" or \
                                    self._board[starting_row + 4][starting_column - 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    elif self._board[starting_row + 4][starting_column - 4] in white_list and \
                            self._board[starting_row + 5][starting_column - 5] is not None:
                        if self._board[starting_row + 4][starting_column - 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 4][starting_column - 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 4][starting_column - 4] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in white_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 0 and starting_column == 7:
                    if start == "Black_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in white_list and \
                                self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "White_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "White_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                                self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "White_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "White_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                                self._board[starting_row + 4][starting_column - 4] in white_list and \
                                self._board[starting_row + 5][starting_column - 5] is not None:
                            if self._board[starting_row + 3][starting_column - 3] == "White_king" or \
                                    self._board[starting_row + 4][starting_column - 4] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 3][starting_column - 3] == "White_Triple_King" or \
                                    self._board[starting_row + 4][starting_column - 4] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 4][starting_column - 4] in white_list and \
                                self._board[starting_row + 5][starting_column - 5] in white_list and \
                                self._board[starting_row + 6][starting_column - 6] is not None:
                            if self._board[starting_row + 4][starting_column - 4] == "White_king" or \
                                    self._board[starting_row + 5][starting_column - 5] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 4][starting_column - 4] == "White_Triple_King" or \
                                    self._board[starting_row + 5][starting_column - 5] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._board[starting_row + 5][starting_column - 5] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 5][starting_column - 5] in white_list and \
                                self._board[starting_row + 6][starting_column - 6] in white_list and \
                                self._board[starting_row + 7][starting_column - 7] is not None:
                            if self._board[starting_row + 5][starting_column - 5] == "White_king" or \
                                    self._board[starting_row + 6][starting_column - 6] == "White_king":
                                player_two.remove_king()
                            if self._board[starting_row + 5][starting_column - 5] == "White_Triple_King" or \
                                    self._board[starting_row + 6][starting_column - 6] == "White_Triple_King":
                                player_two.remove_triple_king()
                            self._board[starting_row + 5][starting_column - 5] = None
                            self._board[starting_row + 6][starting_column - 6] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in white_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in white_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in white_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    elif self._board[starting_row + 4][starting_column - 4] in white_list and \
                            self._board[starting_row + 5][starting_column - 5] is not None:
                        if self._board[starting_row + 4][starting_column - 4] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 4][starting_column - 4] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 4][starting_column - 4] = None
                    elif self._board[starting_row + 5][starting_column - 5] in white_list and \
                            self._board[starting_row + 6][starting_column - 6] is not None:
                        if self._board[starting_row + 5][starting_column - 5] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 5][starting_column - 5] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 5][starting_column - 5] = None
                    elif self._board[starting_row + 6][starting_column - 6] in white_list and \
                            self._board[starting_row + 7][starting_column - 7] is not None:
                        if self._board[starting_row + 6][starting_column - 6] == "White_king":
                            player_two.remove_king()
                        elif self._board[starting_row + 6][starting_column - 6] == "White_Triple_King":
                            player_two.remove_triple_king()
                        self._board[starting_row + 6][starting_column - 6] = None

            # Capture logic for White Kings
            elif start == "White_king" or start == "White_Triple_King":
                self._board[starting_row][starting_column] = None
                self._players[player_name].add_captured_pieces()
                if start == "White_king":
                    self._board[destination_row][destination_column] = "White_king"
                if start == "White_Triple_King":
                    self._board[destination_row][destination_column] = "White_Triple_King"
                if starting_row == 7 and starting_column == 0:
                    if start == "White_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] in black_list and \
                                self._board[starting_row - 5][starting_column + 5] is not None:
                            if self._board[starting_row - 3][starting_column + 3] == "Black_king" or \
                                    self._board[starting_row - 4][starting_column + 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King" or \
                                    self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 4][starting_column + 4] in black_list and \
                                self._board[starting_row - 5][starting_column + 5] in black_list and \
                                self._board[starting_row - 6][starting_column + 6] is not None:
                            if self._board[starting_row - 4][starting_column + 4] == "Black_king" or \
                                    self._board[starting_row - 5][starting_column + 5] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King" or \
                                    self._board[starting_row - 5][starting_column + 5] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._board[starting_row - 5][starting_column + 5] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 5][starting_column + 5] in black_list and \
                                self._board[starting_row - 6][starting_column + 6] in black_list and \
                                self._board[starting_row - 7][starting_column + 7] is not None:
                            if self._board[starting_row - 5][starting_column + 5] == "Black_king" or \
                                    self._board[starting_row - 6][starting_column + 6] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 5][starting_column + 5] == "Black_Triple_King" or \
                                    self._board[starting_row - 6][starting_column + 6] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 5][starting_column + 5] = None
                            self._board[starting_row - 6][starting_column + 6] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    elif self._board[starting_row - 4][starting_column + 4] in black_list and \
                            self._board[starting_row - 5][starting_column + 5] is not None:
                        if self._board[starting_row - 4][starting_column + 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 4][starting_column + 4] = None
                    elif self._board[starting_row - 5][starting_column + 5] in black_list and \
                            self._board[starting_row - 6][starting_column + 6] is not None:
                        if self._board[starting_row - 5][starting_column + 5] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 5][starting_column + 5] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 5][starting_column + 5] = None
                    elif self._board[starting_row - 6][starting_column + 6] in black_list and \
                            self._board[starting_row - 7][starting_column + 7] is not None:
                        if self._board[starting_row - 6][starting_column + 6] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 6][starting_column + 6] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 6][starting_column + 6] = None
                elif starting_row == 7 and starting_column == 2:
                    if start == "White_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] in black_list and \
                                self._board[starting_row - 5][starting_column + 5] is not None:
                            if self._board[starting_row - 3][starting_column + 3] == "Black_king" or \
                                    self._board[starting_row - 4][starting_column + 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King" or \
                                    self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 4][starting_column + 4] in black_list and \
                                self._board[starting_row - 5][starting_column + 5] in black_list and \
                                self._board[starting_row - 6][starting_column + 6] is not None:
                            if self._board[starting_row - 4][starting_column + 4] == "Black_king" or \
                                    self._board[starting_row - 5][starting_column + 5] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King" or \
                                    self._board[starting_row - 5][starting_column + 5] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._board[starting_row - 5][starting_column + 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    elif self._board[starting_row - 4][starting_column + 4] in black_list and \
                            self._board[starting_row - 5][starting_column + 5] is not None:
                        if self._board[starting_row - 4][starting_column + 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 4][starting_column + 4] = None
                elif starting_row == 7 and starting_column == 4:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture up-right double
                        elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                elif starting_row == 7 and starting_column == 6:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] in black_list and \
                                self._board[starting_row - 5][starting_column - 5] is not None:
                            if self._board[starting_row - 3][starting_column - 3] == "Black_king" or \
                                    self._board[starting_row - 4][starting_column - 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King" or \
                                    self._board[starting_row - 4][starting_column - 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._board[starting_row - 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 4][starting_column - 4] in black_list and \
                                self._board[starting_row - 5][starting_column - 5] in black_list and \
                                self._board[starting_row - 6][starting_column - 6] is not None:
                            if self._board[starting_row - 4][starting_column - 4] == "Black_king" or \
                                    self._board[starting_row - 5][starting_column - 5] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 4][starting_column - 4] == "Black_Triple_King" or \
                                    self._board[starting_row - 5][starting_column - 5] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 4][starting_column - 4] = None
                            self._board[starting_row - 5][starting_column - 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    elif self._board[starting_row - 4][starting_column - 4] in black_list and \
                            self._board[starting_row - 5][starting_column - 5] is not None:
                        if self._board[starting_row - 4][starting_column - 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 4][starting_column - 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 4][starting_column - 4] = None
                    elif self._board[starting_row - 5][starting_column - 5] in black_list and \
                            self._board[starting_row - 6][starting_column - 6] is not None:
                        if self._board[starting_row - 5][starting_column - 5] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 5][starting_column - 5] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 5][starting_column - 5] = None
                elif starting_row == 6 and starting_column == 1:
                    if start == "White_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] in black_list and \
                                self._board[starting_row - 5][starting_column + 5] is not None:
                            if self._board[starting_row - 3][starting_column + 3] == "Black_king" or \
                                    self._board[starting_row - 4][starting_column + 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King" or \
                                    self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 4][starting_column + 4] in black_list and \
                                self._board[starting_row - 5][starting_column + 5] in black_list and \
                                self._board[starting_row - 6][starting_column + 6] is not None:
                            if self._board[starting_row - 4][starting_column + 4] == "Black_king" or \
                                    self._board[starting_row - 5][starting_column + 5] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King" or \
                                    self._board[starting_row - 5][starting_column + 5] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._board[starting_row - 5][starting_column + 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    elif self._board[starting_row - 4][starting_column + 4] in black_list and \
                            self._board[starting_row - 5][starting_column + 5] is not None:
                        if self._board[starting_row - 4][starting_column + 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 4][starting_column + 4] = None
                    elif self._board[starting_row - 5][starting_column + 5] in black_list and \
                            self._board[starting_row - 6][starting_column + 6] is not None:
                        if self._board[starting_row - 5][starting_column + 5] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 5][starting_column + 5] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 5][starting_column + 5] = None
                elif starting_row == 6 and starting_column == 3:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture up-right double
                        elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                elif starting_row == 6 and starting_column == 5:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] in black_list and \
                                self._board[starting_row - 5][starting_column - 5] is not None:
                            if self._board[starting_row - 3][starting_column - 3] == "Black_king" or \
                                    self._board[starting_row - 4][starting_column - 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King" or \
                                    self._board[starting_row - 4][starting_column - 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._board[starting_row - 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                if self._board[starting_row - 1][starting_column - 1] in black_list and \
                        self._board[starting_row - 2][starting_column - 2] is not None:
                    if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                        player_one.remove_king()
                    elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                        player_one.remove_triple_king()
                    self._board[starting_row - 1][starting_column - 1] = None
                elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                        self._board[starting_row - 3][starting_column - 3] is not None:
                    if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                        player_one.remove_king()
                    elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                        player_one.remove_triple_king()
                    self._board[starting_row - 2][starting_column - 2] = None
                elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                        self._board[starting_row - 4][starting_column - 4] is not None:
                    if self._board[starting_row - 3][starting_column - 3] == "Black_king":
                        player_one.remove_king()
                    elif self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                        player_one.remove_triple_king()
                    self._board[starting_row - 3][starting_column - 3] = None
                elif self._board[starting_row - 4][starting_column - 4] in black_list and \
                        self._board[starting_row - 5][starting_column - 5] is not None:
                    if self._board[starting_row - 4][starting_column - 4] == "Black_king":
                        player_one.remove_king()
                    elif self._board[starting_row - 4][starting_column - 4] == "Black_Triple_King":
                        player_one.remove_triple_king()
                    self._board[starting_row - 4][starting_column - 4] = None
                    # Capture up-right
                elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                        self._board[starting_row - 2][starting_column + 2] is not None:
                    if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                        player_one.remove_king()
                    elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                        player_one.remove_triple_king()
                    self._board[starting_row - 1][starting_column + 1] = None
                elif starting_row == 6 and starting_column == 7:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] in black_list and \
                                self._board[starting_row - 5][starting_column - 5] is not None:
                            if self._board[starting_row - 3][starting_column - 3] == "Black_king" or \
                                    self._board[starting_row - 4][starting_column - 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King" or \
                                    self._board[starting_row - 4][starting_column - 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._board[starting_row - 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 4][starting_column - 4] in black_list and \
                                self._board[starting_row - 5][starting_column - 5] in black_list and \
                                self._board[starting_row - 6][starting_column - 6] is not None:
                            if self._board[starting_row - 4][starting_column - 4] == "Black_king" or \
                                    self._board[starting_row - 5][starting_column - 5] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 4][starting_column - 4] == "Black_Triple_King" or \
                                    self._board[starting_row - 5][starting_column - 5] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 4][starting_column - 4] = None
                            self._board[starting_row - 5][starting_column - 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    elif self._board[starting_row - 4][starting_column - 4] in black_list and \
                            self._board[starting_row - 5][starting_column - 5] is not None:
                        if self._board[starting_row - 4][starting_column - 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 4][starting_column - 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 4][starting_column - 4] = None
                    elif self._board[starting_row - 5][starting_column - 5] in black_list and \
                            self._board[starting_row - 6][starting_column - 6] is not None:
                        if self._board[starting_row - 5][starting_column - 5] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 5][starting_column - 5] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 5][starting_column - 5] = None
                elif starting_row == 5 and starting_column == 0:
                    if start == "White_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] in black_list and \
                                self._board[starting_row - 5][starting_column + 5] is not None:
                            if self._board[starting_row - 3][starting_column + 3] == "Black_king" or \
                                    self._board[starting_row - 4][starting_column + 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King" or \
                                    self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    elif self._board[starting_row - 4][starting_column + 4] in black_list and \
                            self._board[starting_row - 5][starting_column + 5] is not None:
                        if self._board[starting_row - 4][starting_column + 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 4][starting_column + 4] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 5 and starting_column == 2:
                    if start == "White_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] in black_list and \
                                self._board[starting_row - 5][starting_column + 5] is not None:
                            if self._board[starting_row - 3][starting_column + 3] == "Black_king" or \
                                    self._board[starting_row - 4][starting_column + 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King" or \
                                    self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._board[starting_row - 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    elif self._board[starting_row - 4][starting_column + 4] in black_list and \
                            self._board[starting_row - 5][starting_column + 5] is not None:
                        if self._board[starting_row - 4][starting_column + 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 4][starting_column + 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 4][starting_column + 4] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 5 and starting_column == 4:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture up-right double
                        elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                        # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                        # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 5 and starting_column == 6:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] in black_list and \
                                self._board[starting_row - 5][starting_column - 5] is not None:
                            if self._board[starting_row - 3][starting_column - 3] == "Black_king" or \
                                    self._board[starting_row - 4][starting_column - 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King" or \
                                    self._board[starting_row - 4][starting_column - 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                                self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    elif self._board[starting_row - 4][starting_column - 4] in black_list and \
                            self._board[starting_row - 5][starting_column - 5] is not None:
                        if self._board[starting_row - 4][starting_column - 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 4][starting_column - 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 4][starting_column - 4] = None
                    elif self._board[starting_row - 5][starting_column - 5] in black_list and \
                            self._board[starting_row - 6][starting_column - 6] is not None:
                        if self._board[starting_row - 5][starting_column - 5] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 5][starting_column - 5] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 5][starting_column - 5] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                elif starting_row == 4 and starting_column == 1:
                    if start == "White_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                elif starting_row == 4 and starting_column == 3:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture up-right double
                        elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] in black_list and \
                                self._board[starting_row - 4][starting_column + 4] is not None:
                            if self._board[starting_row - 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._board[starting_row - 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-left double
                        elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    elif self._board[starting_row - 3][starting_column + 3] in black_list and \
                            self._board[starting_row - 4][starting_column + 4] is not None:
                        if self._board[starting_row - 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column + 3] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                elif starting_row == 4 and starting_column == 5:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-left double
                        elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                        # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 4 and starting_column == 7:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] in black_list and \
                                self._board[starting_row - 4][starting_column - 4] is not None:
                            if self._board[starting_row - 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._board[starting_row - 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-left double
                        elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    elif self._board[starting_row - 3][starting_column - 3] in black_list and \
                            self._board[starting_row - 4][starting_column - 4] is not None:
                        if self._board[starting_row - 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 3][starting_column - 3] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                elif starting_row == 3 and starting_column == 0:
                    if start == "White_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                elif starting_row == 3 and starting_column == 2:
                    if start == "White_Triple_King":
                        # Capture up-right double
                        if self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                elif starting_row == 3 and starting_column == 4:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture up-right double
                        elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                                self._board[starting_row - 2][starting_column + 2] in black_list and \
                                self._board[starting_row - 3][starting_column + 3] is not None:
                            if self._board[starting_row - 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column + 1] = None
                            self._board[starting_row - 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-left double
                        elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    elif self._board[starting_row - 2][starting_column + 2] in black_list and \
                            self._board[starting_row - 3][starting_column + 3] is not None:
                        if self._board[starting_row - 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column + 2] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                elif starting_row == 3 and starting_column == 6:
                    if start == "White_Triple_King":
                        # Capture up-left double
                        if self._board[starting_row - 1][starting_column - 1] in black_list and \
                                self._board[starting_row - 2][starting_column - 2] in black_list and \
                                self._board[starting_row - 3][starting_column - 3] is not None:
                            if self._board[starting_row - 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row - 1][starting_column - 1] = None
                            self._board[starting_row - 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-left double
                        elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    elif self._board[starting_row - 2][starting_column - 2] in black_list and \
                            self._board[starting_row - 3][starting_column - 3] is not None:
                        if self._board[starting_row - 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 2][starting_column - 2] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                elif starting_row == 2 and starting_column == 1:
                    if start == "White_Triple_King":
                        # Capture down-right double
                        if self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] in black_list and \
                                self._board[starting_row + 5][starting_column + 5] is not None:
                            if self._board[starting_row + 3][starting_column + 3] == "Black_king" or \
                                    self._board[starting_row + 4][starting_column + 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King" or \
                                    self._board[starting_row + 4][starting_column + 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-right
                    if self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                    elif self._board[starting_row + 4][starting_column + 4] in black_list and \
                            self._board[starting_row + 5][starting_column + 5] is not None:
                        if self._board[starting_row + 4][starting_column + 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 4][starting_column + 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 4][starting_column + 4] = None
                elif starting_row == 2 and starting_column == 3:
                    if start == "White_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                elif starting_row == 2 and starting_column == 5:
                    if start == "White_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] in black_list and \
                                self._board[starting_row + 5][starting_column - 5] is not None:
                            if self._board[starting_row + 3][starting_column - 3] == "Black_king" or \
                                    self._board[starting_row + 4][starting_column - 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King" or \
                                    self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture up-right
                    elif self._board[starting_row - 1][starting_column + 1] in black_list and \
                            self._board[starting_row - 2][starting_column + 2] is not None:
                        if self._board[starting_row - 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column + 1] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    elif self._board[starting_row + 4][starting_column - 4] in black_list and \
                            self._board[starting_row + 5][starting_column - 5] is not None:
                        if self._board[starting_row + 4][starting_column - 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 4][starting_column - 4] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 2 and starting_column == 7:
                    if start == "White_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] in black_list and \
                                self._board[starting_row + 5][starting_column - 5] is not None:
                            if self._board[starting_row + 3][starting_column - 3] == "Black_king" or \
                                    self._board[starting_row + 4][starting_column - 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King" or \
                                    self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture up-left
                    if self._board[starting_row - 1][starting_column - 1] in black_list and \
                            self._board[starting_row - 2][starting_column - 2] is not None:
                        if self._board[starting_row - 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row - 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row - 1][starting_column - 1] = None
                    # Capture down-left
                    elif self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    elif self._board[starting_row + 4][starting_column - 4] in black_list and \
                            self._board[starting_row + 5][starting_column - 5] is not None:
                        if self._board[starting_row + 4][starting_column - 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 4][starting_column - 4] = None
                elif starting_row == 1 and starting_column == 0:
                    if start == "White_Triple_King":
                        # Capture down-right double
                        if self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] in black_list and \
                                self._board[starting_row + 5][starting_column + 5] is not None:
                            if self._board[starting_row + 3][starting_column + 3] == "Black_king" or \
                                    self._board[starting_row + 4][starting_column + 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King" or \
                                    self._board[starting_row + 4][starting_column + 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 4][starting_column + 4] in black_list and \
                                self._board[starting_row + 5][starting_column + 5] in black_list and \
                                self._board[starting_row + 6][starting_column + 6] is not None:
                            if self._board[starting_row + 4][starting_column + 4] == "Black_king" or \
                                    self._board[starting_row + 5][starting_column + 5] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 4][starting_column + 4] == "Black_Triple_King" or \
                                    self._board[starting_row + 5][starting_column + 5] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._board[starting_row + 5][starting_column + 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-right
                    if self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                    elif self._board[starting_row + 4][starting_column + 4] in black_list and \
                            self._board[starting_row + 5][starting_column + 5] is not None:
                        if self._board[starting_row + 4][starting_column + 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 4][starting_column + 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 4][starting_column + 4] = None
                    elif self._board[starting_row + 5][starting_column + 5] in black_list and \
                            self._board[starting_row + 6][starting_column + 6] is not None:
                        if self._board[starting_row + 5][starting_column + 5] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 5][starting_column + 5] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 5][starting_column + 5] = None
                elif starting_row == 1 and starting_column == 2:
                    if start == "White_Triple_King":
                        # Capture down-right double
                        if self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] in black_list and \
                                self._board[starting_row + 5][starting_column + 5] is not None:
                            if self._board[starting_row + 3][starting_column + 3] == "Black_king" or \
                                    self._board[starting_row + 4][starting_column + 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King" or \
                                    self._board[starting_row + 4][starting_column + 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                    elif self._board[starting_row + 4][starting_column + 4] in black_list and \
                            self._board[starting_row + 5][starting_column + 5] is not None:
                        if self._board[starting_row + 4][starting_column + 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 4][starting_column + 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 4][starting_column + 4] = None
                elif starting_row == 1 and starting_column == 4:
                    if start == "White_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                elif starting_row == 1 and starting_column == 6:
                    if start == "White_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] in black_list and \
                                self._board[starting_row + 5][starting_column - 5] is not None:
                            if self._board[starting_row + 3][starting_column - 3] == "Black_king" or \
                                    self._board[starting_row + 4][starting_column - 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King" or \
                                    self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 4][starting_column - 4] in black_list and \
                                self._board[starting_row + 5][starting_column - 5] in black_list and \
                                self._board[starting_row + 6][starting_column - 6] is not None:
                            if self._board[starting_row + 4][starting_column - 4] == "Black_king" or \
                                    self._board[starting_row + 5][starting_column - 5] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King" or \
                                    self._board[starting_row + 5][starting_column - 5] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._board[starting_row + 5][starting_column - 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    elif self._board[starting_row + 4][starting_column - 4] in black_list and \
                            self._board[starting_row + 5][starting_column - 5] is not None:
                        if self._board[starting_row + 4][starting_column - 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 4][starting_column - 4] = None
                    elif self._board[starting_row + 5][starting_column - 5] in black_list and \
                            self._board[starting_row + 6][starting_column - 6] is not None:
                        if self._board[starting_row + 5][starting_column - 5] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 5][starting_column - 5] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 5][starting_column - 5] = None
                elif starting_row == 0 and starting_column == 1:
                    if start == "White_Triple_King":
                        # Capture down-right double
                        if self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] in black_list and \
                                self._board[starting_row + 5][starting_column + 5] is not None:
                            if self._board[starting_row + 3][starting_column + 3] == "Black_king" or \
                                    self._board[starting_row + 4][starting_column + 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King" or \
                                    self._board[starting_row + 4][starting_column + 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 4][starting_column + 4] in black_list and \
                                self._board[starting_row + 5][starting_column + 5] in black_list and \
                                self._board[starting_row + 6][starting_column + 6] is not None:
                            if self._board[starting_row + 4][starting_column + 4] == "Black_king" or \
                                    self._board[starting_row + 5][starting_column + 5] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 4][starting_column + 4] == "Black_Triple_King" or \
                                    self._board[starting_row + 5][starting_column + 5] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 4][starting_column + 4] = None
                            self._board[starting_row + 5][starting_column + 5] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-right
                    if self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                    elif self._board[starting_row + 4][starting_column + 4] in black_list and \
                            self._board[starting_row + 5][starting_column + 5] is not None:
                        if self._board[starting_row + 4][starting_column + 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 4][starting_column + 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 4][starting_column + 4] = None
                    elif self._board[starting_row + 5][starting_column + 5] in black_list and \
                            self._board[starting_row + 6][starting_column + 6] is not None:
                        if self._board[starting_row + 5][starting_column + 5] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 5][starting_column + 5] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 5][starting_column + 5] = None
                elif starting_row == 0 and starting_column == 3:
                    if start == "White_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        # Capture down-right double
                        elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                                self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] is not None:
                            if self._board[starting_row + 1][starting_column + 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column + 1] = None
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                                self._board[starting_row + 3][starting_column + 3] in black_list and \
                                self._board[starting_row + 4][starting_column + 4] is not None:
                            if self._board[starting_row + 2][starting_column + 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column + 2] = None
                            self._board[starting_row + 3][starting_column + 3] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                    elif self._board[starting_row + 2][starting_column + 2] in black_list and \
                            self._board[starting_row + 3][starting_column + 3] is not None:
                        if self._board[starting_row + 2][starting_column + 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column + 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column + 2] = None
                    elif self._board[starting_row + 3][starting_column + 3] in black_list and \
                            self._board[starting_row + 4][starting_column + 4] is not None:
                        if self._board[starting_row + 3][starting_column + 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column + 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column + 3] = None
                elif starting_row == 0 and starting_column == 5:
                    if start == "White_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] in black_list and \
                                self._board[starting_row + 5][starting_column - 5] is not None:
                            if self._board[starting_row + 3][starting_column - 3] == "Black_king" or \
                                    self._board[starting_row + 4][starting_column - 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King" or \
                                    self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    elif self._board[starting_row + 4][starting_column - 4] in black_list and \
                            self._board[starting_row + 5][starting_column - 5] is not None:
                        if self._board[starting_row + 4][starting_column - 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 4][starting_column - 4] = None
                    # Capture down-right
                    elif self._board[starting_row + 1][starting_column + 1] in black_list and \
                            self._board[starting_row + 2][starting_column + 2] is not None:
                        if self._board[starting_row + 1][starting_column + 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column + 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column + 1] = None
                elif starting_row == 0 and starting_column == 7:
                    if start == "White_Triple_King":
                        # Capture down-left double
                        if self._board[starting_row + 1][starting_column - 1] in black_list and \
                                self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] is not None:
                            if self._board[starting_row + 1][starting_column - 1] == "Black_king" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King" or \
                                    self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 1][starting_column - 1] = None
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                                self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] is not None:
                            if self._board[starting_row + 2][starting_column - 2] == "Black_king" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King" or \
                                    self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 2][starting_column - 2] = None
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                                self._board[starting_row + 4][starting_column - 4] in black_list and \
                                self._board[starting_row + 5][starting_column - 5] is not None:
                            if self._board[starting_row + 3][starting_column - 3] == "Black_king" or \
                                    self._board[starting_row + 4][starting_column - 4] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King" or \
                                    self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 3][starting_column - 3] = None
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 4][starting_column - 4] in black_list and \
                                self._board[starting_row + 5][starting_column - 5] in black_list and \
                                self._board[starting_row + 6][starting_column - 6] is not None:
                            if self._board[starting_row + 4][starting_column - 4] == "Black_king" or \
                                    self._board[starting_row + 5][starting_column - 5] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King" or \
                                    self._board[starting_row + 5][starting_column - 5] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 4][starting_column - 4] = None
                            self._board[starting_row + 5][starting_column - 5] = None
                            self._players[player_name].add_captured_pieces()
                        elif self._board[starting_row + 5][starting_column - 5] in black_list and \
                                self._board[starting_row + 6][starting_column - 6] in black_list and \
                                self._board[starting_row + 7][starting_column - 7] is not None:
                            if self._board[starting_row + 5][starting_column - 5] == "Black_king" or \
                                    self._board[starting_row + 6][starting_column - 6] == "Black_king":
                                player_one.remove_king()
                            if self._board[starting_row + 5][starting_column - 5] == "Black_Triple_King" or \
                                    self._board[starting_row + 6][starting_column - 6] == "Black_Triple_King":
                                player_one.remove_triple_king()
                            self._board[starting_row + 5][starting_column - 5] = None
                            self._board[starting_row + 6][starting_column - 6] = None
                            self._players[player_name].add_captured_pieces()

                    # Capture down-left
                    if self._board[starting_row + 1][starting_column - 1] in black_list and \
                            self._board[starting_row + 2][starting_column - 2] is not None:
                        if self._board[starting_row + 1][starting_column - 1] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 1][starting_column - 1] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 1][starting_column - 1] = None
                    elif self._board[starting_row + 2][starting_column - 2] in black_list and \
                            self._board[starting_row + 3][starting_column - 3] is not None:
                        if self._board[starting_row + 2][starting_column - 2] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 2][starting_column - 2] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 2][starting_column - 2] = None
                    elif self._board[starting_row + 3][starting_column - 3] in black_list and \
                            self._board[starting_row + 4][starting_column - 4] is not None:
                        if self._board[starting_row + 3][starting_column - 3] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 3][starting_column - 3] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 3][starting_column - 3] = None
                    elif self._board[starting_row + 4][starting_column - 4] in black_list and \
                            self._board[starting_row + 5][starting_column - 5] is not None:
                        if self._board[starting_row + 4][starting_column - 4] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 4][starting_column - 4] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 4][starting_column - 4] = None
                    elif self._board[starting_row + 5][starting_column - 5] in black_list and \
                            self._board[starting_row + 6][starting_column - 6] is not None:
                        if self._board[starting_row + 5][starting_column - 5] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 5][starting_column - 5] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 5][starting_column - 5] = None
                    elif self._board[starting_row + 6][starting_column - 6] in black_list and \
                            self._board[starting_row + 7][starting_column - 7] is not None:
                        if self._board[starting_row + 6][starting_column - 6] == "Black_king":
                            player_one.remove_king()
                        elif self._board[starting_row + 6][starting_column - 6] == "Black_Triple_King":
                            player_one.remove_triple_king()
                        self._board[starting_row + 6][starting_column - 6] = None
