# Author: Kevin Braman
# GitHub username: kevinbraman92
# Date: 03/29/2023
# Description: This program defines two classes: "Checkers" and "Player". The Checkers class represents a game of
#              checkers played by two people. The Checkers class creates and contains Player objects, who in turn
#              contain data members that store player-specific information regarding the game. Each player has 12
#              pieces which can be upgraded to "King" or "Triple King" status. If a player loses all their pieces,
#              the game ends. This program imports capture and movement logic from the "CheckerGameLogic" module.
#              The program assumes the player knows the rules of the game and will not intentionally attempt to break
#              them.

from CheckerGameLogic import GameLogic


class OutOfTurn(Exception):
    """
    This exception is raised within the Checkers object when a player attempts to make a move outside their turn.
    Used by the following method: play_game
    """
    pass


class InvalidSquare(IndexError):
    """
     This exception is raised within the Checkers object when a player makes an illegal move.
     Used by the following methods: play_game, get_checker_details
    """
    pass


class InvalidPlayer(Exception):
    """
    This exception is raised within the Checkers object when a non-player attempts to make a move.
    Used by the following method: play_game
    """
    pass


class Player:
    """Represents a player of the board game checkers."""

    def __init__(self, player_name, checker_color):
        """
        Constructor method that takes the following parameters:

        player_name     = string containing the player's name
        checker_color   = string containing the color chosen by the player, either "Black" or "White"

        The following private data members are initialized:

        captured_pieces = the count of pieces captured, initialized to 0
        kings           = the count of active kings, initialized to 0
        triple_kings    = the count of active triple_kings, initialized to 0
        """
        self._player_name = player_name
        self._checker_color = checker_color
        self._captured_pieces = 0
        self._kings = 0
        self._triple_kings = 0

    def get_name(self):
        """Class method that returns the string name of the Player object."""
        return self._player_name

    def get_checker_color(self):
        """Class method that returns the string color of the Player object."""
        return self._checker_color

    def get_captured_pieces_count(self):
        """Class method that returns the count of captured pieces."""
        return self._captured_pieces

    def get_king_count(self):
        """Class method that returns the count of active kings."""
        return self._kings

    def get_triple_king_count(self):
        """Class method that returns the count of active triple kings."""
        return self._triple_kings

    def add_captured_pieces(self):
        """Class method that adds to the captured_pieces data member."""
        self._captured_pieces += 1

    def add_king(self):
        """Class method that adds to the kings data member."""
        self._kings += 1

    def remove_king(self):
        """Class method that removes from the kings data member."""
        self._kings -= 1

    def add_triple_king(self):
        """Class method that adds to the triple_kings data member."""
        self._triple_kings += 1

    def remove_triple_king(self):
        """Class method that removes from the triple_kings data member."""
        self._triple_kings -= 1

    def __str__(self):
        """The default string representation of a Player object."""
        return f"{self._player_name}, {self._checker_color}"


class Checkers(GameLogic):
    """Represents the game checkers with two players."""

    def __init__(self):
        """
        Constructor method that takes no parameters.

        This constructor inherits the following data members of the "GameLogic" class:

        capture_state   = if a piece can capture, this will be boolean True, otherwise defaulted to boolean False
        players         = initialized as an empty dictionary, stores player objects using the create_player method
        board           = creates a list of lists that represents the board. The board can be printed out using the
                          print_board method. 12 squares on the top have the string "White", on the bottom 12 squares
                          have the string "Black". These are the pieces used by the player. The remaining spaces are
                          element positions containing None.

        In addition, the following private data members are initialized:

        turn            = the string turn of the current player, defaulted to "Black"
        game_won        = if any player captures 12 pieces, the game is won. Defaults to boolean False
        """
        super().__init__()
        self._turn = "Black"
        self._game_won = False

    def create_player(self, player_name, piece_color):
        """
        Class method that takes two parameters:
        player_name     = string containing the player name
        piece_color     = string containing the color picked by the player

        This method creates Player objects and stores them in the class data member players. This data member is a
        dictionary and the player name is used as they key.
        """
        player = Player(player_name, piece_color)
        self._players[player_name] = player
        return player

    def get_players(self):
        """Class method that returns the dictionary in the class data member players."""
        return self._players

    def get_turn(self):
        """Class method that returns the current string turn stored in the class data member turn."""
        return self._turn

    def play_game(self, player_name, starting_square_location, destination_square_location):
        """
        This class method takes three parameters:
        player name                 = string name of the player making the move, corresponding with the key-name in
                                      the players dictionary
        starting_square_location    = a tuple in (x,y) format, the square the player is moving from
        destination_square_location = a tuple in (x,y) format, the square the player is moving to

        This method calls upon the various methods of the parent class 'GameLogic' in its execution. The method's
        execution is as follows:

        1. Check exception cases
        2. Check if the game is won
        3. Call the method 'make_move' from parent class 'GameLogic' to move the piece
        4. Call the method 'upgrade_piece' from parent class 'GameLogic' to upgrade a piece if possible
        5. Call the method 'can_capture' from the parent class 'GameLogic' check if a capturing piece can capture again
        6. Change turn if 'can_capture' is false, otherwise pass
        7. Return the user's captured pieces.


        If the tuples in either starting_square_location or destination_square_location are outside the board,
        an InvalidSquare Exception is raised. If a player attempts to move outside their turn, an OutOfTurn Exception
        is raised. If a player attempts to select a piece not of their side's color, an InvalidSquare Exception is
        raised. If a player_name is used that is not within the players data member, an InvalidPlayer Exception is
        raised.

        This method returns the count of captured pieces for the player making the move.
        """

        # Define local variables
        starting_row, starting_column = starting_square_location[0], starting_square_location[1]
        destination_row, destination_column = destination_square_location[0], destination_square_location[1]
        start = self.get_checker_details(starting_square_location)

        # Exception cases
        if player_name not in self._players:
            raise InvalidPlayer

        if starting_row > 7 or starting_column > 7 or destination_row > 7 or destination_column > 7:
            raise InvalidSquare

        if self._players[player_name].get_checker_color() != self._turn:
            raise OutOfTurn

        if start != self._players[player_name].get_checker_color():
            if self._players[player_name].get_checker_color() == "Black" and \
                    start != "Black" and start != "Black_king" and start != "Black_Triple_King":
                raise InvalidSquare
            if self._players[player_name].get_checker_color() == "White" and \
                    start != "White" and start != "White_king" and start != "White_Triple_King":
                raise InvalidSquare

        # Check if game is won
        if self._players[player_name].get_captured_pieces_count() == 12:
            self._game_won = True
            return self.game_winner()

        # Move piece
        self.make_move(player_name, starting_square_location, destination_square_location)

        # Upgrade piece if possible
        self.upgrade_piece(player_name, starting_square_location, destination_square_location)

        # Check capture state
        if self._capture_state is True:
            if self.can_capture(destination_square_location) is True:
                pass
            else:
                self._capture_state = False

        # Change turn if piece cannot capture
        if self._turn == "Black" and self._capture_state is False:
            self._turn = "White"
        elif self._turn == "White" and self._capture_state is False:
            self._turn = "Black"

        return self._players[player_name].get_captured_pieces_count()

    def print_board(self):
        """This class method takes no parameters and prints out the playing board."""
        for rows in self._board:
            print(rows)

    def game_winner(self):
        """
        This class method takes no parameters and either returns a message stating the game has not ended if the
        class data member game_won is False or returns the name of the winning player if game_won is True. This method
        is called during the execution of the play_game method if a player captures 12 pieces.
        """
        if self._game_won is False:
            return "Game has not ended."
        else:
            for players in self._players:
                players_object = self._players[players]
                if players_object.get_checker_color() == self._turn:
                    return f"{players_object.get_name()} has won the game!"

    def print_rules(self):
        """This class method prints out the rules of the game."""
        print("\n")
        print("GAME RULES")
        print("There are two players, 'Black' and 'White'. Each player has 12 pieces. Player 'Black' moves first.")
        print("All pieces start as pawns. Pawns may only move & capture diagonally forwards.")
        print("If a piece makes it to the opposite end, it will upgrade to a king.")
        print("If it makes it back again to its side's board end, it will upgrade to a triple king.")
        print("King pieces can move and capture diagonally in any direction. They do not have to be adjacent to "
              "capture.")
        print("Triple kings can do everything a king can, as well as jump friendly pieces to move faster and double "
              "capture.")
        print("If a piece can capture, it must capture. If a piece captures and can capture again, it must capture.")
        print("The game ends when a player has captured all opposing pieces.")
        print("\n")


def main():
    game = Checkers()
    game.print_rules()
    game.print_board()


if __name__ == "__main__":
    main()
