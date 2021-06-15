# Author: Marc Zalik
# Date: 2021-05-20
# Description: An interactive, two-player, command-line version of the classic marble game Kuba.

class KubaGame:
    """
    A representation of a game of Kuba. Manages the overall state of the game, including whose turn it is, what the
    previous versions of the board were, and who has won. Communicates with an instance of KubaBoard to handle move
    validation and updating the board, and two instance of KubaPlayer to handle name, color, and marble capture checking.
    """
    def __init__(self, player_1, player_2):
        """
        Initializes a new game of Kuba.
        :param player_1: Tuple (String, String): Player name, Color.
        :param player_2: Tuple (String, String): Player name, Color.
        """
        self._player_1 = KubaPlayer(player_1)
        self._player_2 = KubaPlayer(player_2)
        self._turn = None
        self._winner = None
        self._captured_marbles = dict()
        self._player_1_prev_board_state = None
        self._player_1_prev_player_state = None
        self._player_2_prev_board_state = None
        self._player_2_prev_player_state = None
        self._board = KubaBoard()

    def get_current_turn(self):
        """
        Returns the name of the player whose turn it currently is. If no player has gone yet, returns None.
        :return: String, the name of the current player. Returns None if no player has gone yet.
        """
        # Match _turn to playername.
        if self._turn == 0:
            return self._player_1.get_playername()
        elif self._turn == 1:
            return self._player_2.get_playername()
        # No moves have been made, _turn == None.
        else:
            return self._turn

    def get_winner(self):
        """
        Returns the name of the winning player. Returns None if no winner yet.
        :return: String, the name of the winning player. Returns None if no player has won.
        """
        return self._winner

    def get_captured(self, playername):
        """
        Returns the number of Red marbles that playername has captured.
        :param playername: String, the name of a player.
        :return: Integer, the number of Red marbles captured by playername.
        """
        # Match playername to _player_1 or _player_2. Default to None if no match.
        player = self._player_1 if self._player_1.get_playername() == playername else self._player_2 \
            if self._player_2.get_playername() == playername else None

        if player is not None:
            return player.get_captured_marbles()

    def get_marble(self, coordinates):
        """
        Returns the color of the marble at the given coordinates.
        :param coordinates: Tuple (Integer, Integer)
        :return: String, the color of the marble at the coordinates.
        """
        # Request marble from _board.
        response = self._board.return_marble(coordinates)
        if response is None:
            response = 'X'
        return response

    def get_marble_count(self):
        """
        Returns a tuple giving the count of each color of marble on the board in the order (W, B, R).
        :return: Tuple (Int, Int, Int), the counts of each color of marble on the board.
        """
        # Request count from _board.
        return self._board.get_marbles()

    def make_move(self, playername, coordinates, direction):
        """
        Given a player, a coordinate on the board, and a direction, attempts to push the marble in that direction. Checks
        for validity of movement according to the game rules, and returns False if the move made is illegal in any way.
        Otherwise, updates the board and player states along with the turn counter.
        :param playername: String, the name of the player to make a move for.
        :param coordinates: Tuple (Int, Int). Location of the marble to move. Must be on the game board.
        :param direction: String, direction to push the marble in. 'L' = Left, 'R' = Right, 'F' = Forward, 'B' = Backward.
        :return: True or False, was the move legal.
        """
        # Someone has won already.
        if self._winner is not None:
            return False

        # If any opponent marble is pushed off it is removed from the board.
        # If a Red marble is pushed off it is considered captured by the player who made the move.
        # If the move is successful, this method should return True.
        # If the move is being made after the game has been won, or when it's not the player's turn or if the
            # coordinates provided are not valid or a marble in the coordinates cannot be moved in the direction
            # specified or it is not the player's marble or for any other invalid conditions return False.

        # Not player's turn.
        if self.get_current_turn() is not None and playername != self.get_current_turn():
            return False

        # Match playername to _player_1 or _player_2. Defaults to None if name not recognized.
        player = self._player_1 if self._player_1.get_playername() == playername else self._player_2 \
            if self._player_2.get_playername() == playername else None

        # Check that the move is valid and update the board state if it is.
        if self._board.validate_move(coordinates, direction, player):
            self._board.move_marble(coordinates, direction, player)
        else:
            return False

        # KO CHECK
        # Check to make sure that the current game state is not the same as it was at the end of my last turn. If they
        # are the same, that means I undid the other player's move, which is illegal. If so, reset the board to the
        # state it was in at the end of the other player's turn. Also reset the captured marble counts.
        if self._board.get_state() == self._get_prev_board_state():
            self._board.set_state(self._reset_board_state())
            player.set_captured_marbles(self._get_prev_player_state())
            return False

        # Move finalized, update the state of board at the end of my turn to use for Ko Check during my next turn.
        self._update_state(player)

        # Swap players.
        self._update_turn(playername)

        # Check for win conditions and update appropriately.
        # has_won() uses _get_current_player as the turn has already been updated and we need a reference to both player
        # objects in order to 1) check for the next player's possible valid moves and 2) update the winner to the current
        # player's name if necessary.
        if self._board.has_won(player, self._get_current_player()):
            self._winner = player.get_playername()

        return True

    def _get_current_player(self):
        """
        Returns the player object for the current turn.
        :return: Player object, the current player.
        """
        if self._turn == 0:
            return self._player_1
        elif self._turn == 1:
            return self._player_2

    def _get_player_turn(self, player):
        """
        Given a player object, matches the player to their turn.
        :param player: Player object.
        :return: Integer, the turn counter value for that player's turn.
        """
        if player == self._player_1:
            return 0
        elif player == self._player_2:
            return 1

    def _get_prev_board_state(self):
        """
        Returns a deep copy of _board._spaces as it existed at the end of the current player's last turn.
        :return: List of List of Strings, otherwise None if no one has gone yet.
        """
        if self._turn == 0:
            return self._player_1_prev_board_state
        elif self._turn == 1:
            return self._player_2_prev_board_state
        else:
            return None

    def _get_prev_player_state(self):
        """
        Returns the number of Red marbles captured by the previous player at the end of the previous player's turn.
        :return: Integer, otherwise None if no one has gone yet.
        """
        if self._turn == 0:
            return self._player_1_prev_player_state
        elif self._turn == 1:
            return self._player_2_prev_player_state
        else:
            return None

    def _reset_board_state(self):
        """
        Returns a deep copy of _board._spaces as it existed at the end of the previous player's turn.
        :return: List of List of Strings, otherwise None if no one has gone yet.
        """
        if self._turn == 0:
            return self._player_2_prev_board_state
        elif self._turn == 1:
            return self._player_1_prev_board_state
        else:
            return None

    def _update_state(self, player):
        """
        Updates the state of the current player's previous game states as they exist at the end of their current turn.
        :return: Nothing.
        """
        if self._get_player_turn(player) == 0:
        # if self._turn == 0:
            self._player_1_prev_board_state = self._board.get_state()
            self._player_1_prev_player_state = self._player_1.get_captured_marbles()
        elif self._get_player_turn(player) == 1:
        # elif self._turn == 1:
            self._player_2_prev_board_state = self._board.get_state()
            self._player_2_prev_player_state = self._player_2.get_captured_marbles()

    def _update_turn(self, player):
        """
        Updates the turn counter to track whose turn it is. If no one has gone yet, sets _turn to the current player and
        continues with the normal update procedure.
        :param player: String, the name of a player.
        :return: Nothing, otherwise returns False if invalid update made.
        """
        # _player_1 is always _turn = 0 and _player_2 is always _turn = 1, regardless of who actually goes first.
        if self._turn is None:
            if player == self._player_1.get_playername():
                self._turn = 0
            elif player == self._player_2.get_playername():
                self._turn = 1
            # Invalid player, don't update turn
            else:
                return False

        # Set _turn to 0 for player 1 or 1 for player 2
        self._turn = (self._turn + 1) % 2


class KubaBoard:
    """
    A representation of the Kuba board. Maintains the state of the board, including marble locations, validates moves,
    and moves marbles. Communicates with the KubaGame to send it information about the state of the board and whether
    moves are valid, and with the KubaPlayers to check their name and color.
    """
    def __init__(self):
        """
        Initializes a new Kuba board.
        """
        self._spaces = [[None] * 7 for num in range(7)]
        # Coordinate vectors representing the direction of a given push:
        self._left = (0,-1)
        self._right = (0,1)
        self._forward = (-1,0)
        self._backward = (1,0)
        # Map directions to vectors:
        self._moves = {'L': self._left, 'R': self._right, 'F': self._forward, 'B': self._backward}
        self.initialize_marbles()

    def get_state(self):
        """
        Returns a deep copy of the locations on the board.
        :return: List of List of Strings.
        """
        return [row[:] for row in self._spaces]

    def set_state(self, state):
        """
        Sets the state of the board spaces. For use in resetting the board when Ko has occurred.
        :param state: List of List of Strings.
        :return: Nothing.
        """
        self._spaces = [row[:] for row in state]

    def initialize_marbles(self):
        """
        Sets the default marble locations on the board. Pictorially, the board looks like:
        _________________________________
        |	W	W	X	X	X	B	B	|
        |	W	W	X	R	X	B	B	|
        |	X	X	R	R	R	X	X	|
        |	X	R	R	R	R	R	X	|
        |	X	X	R	R	R	X	X	|
        |	B	B	X	R	X	W	W	|
        |	B	B	X	X	X	W	W	|
        ---------------------------------
        """
        # Starting marble locations.
        starting_marbles = {'W': [(0,0),(0,1),(1,0),(1,1),(5,5),(5,6),(6,5),(6,6)],
                            'B': [(0,5),(0,6),(1,5),(1,6),(5,0),(5,1),(6,0),(6,1)],
                            'R': [(1,3),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(3,4),(3,5),(4,2),(4,3),(4,4),(5,3)]}

        # Set each location on the board to its appropriate marble color.
        for marble in starting_marbles.keys():
            for location in starting_marbles[marble]:
                self._spaces[location[0]][location[1]] = marble

    def display_board(self):
        """
        Displays the current game board on the command line.
        :return: Nothing.
        """
        print("_"*33, end="")
        print(" "*33, end="")
        print()
        for row in self._spaces:
            print('|', end='\t')
            for column in row:
                if column is not None:
                    print(column, end='\t')
                else:
                    print('X', end='\t')
            print('|')
        print("-"*33, end="")
        print()

    def validate_move(self, coordinates, direction, player):
        """
        Given a location of a marble, a direction to push the marble, and a player, validates whether the move is legal
        according to the rules of Kuba. Returns whether the move is valid.
        :param coordinates: Tuple (Int, Int), a location of a marble.
        :param direction: String, the direction to push the marble. 'L' = Left, 'R' = Right, 'F' = Forward, 'B' = Backward.
        :param player: Player object, the player making the move.
        :return: True or False, is the given move valid.
        """
        if not self.is_on_board(coordinates):
            return False

        # Location points to an empty spot on the board.
        if self._spaces[coordinates[0]][coordinates[1]] is None:
            return False

        # Location points to a marble that is not the player's color.
        if self._spaces[coordinates[0]][coordinates[1]] != player.get_color():
            return False

        # Not a valid starting position.
        if not self.valid_start_position(coordinates, direction, player):
            return False

        # Everything to this point is valid. Validity of the move depends only on the validity of the ending position.
        return self.valid_end_position(coordinates, direction, player)

    def valid_start_position(self, coordinates, direction, player):
        """
        Given a location of a marble, a direction to push the marble, and a player, validates whether the beginning
        position of the move is legal according to the rules of Kuba. Returns whether the starting position is valid.
        :param coordinates: Tuple (Int, Int), a location of a marble.
        :param direction: String, the direction to push the marble. 'L' = Left, 'R' = Right, 'F' = Forward, 'B' = Backward.
        :param player: Player object, the player making the move.
        :return: True or False, is the given starting position valid.
        """
        # Match the direction of the push to its momentum vector.
        momentum = self._moves[direction]

        # Apply the negative of the momentum vector to determine where the push is coming from.
        push_coords = (coordinates[0]+momentum[0]*-1, coordinates[1]+momentum[1]*-1)

        # Push is coming from off the board, automatically legal
        if not self.is_on_board(push_coords):
            return True

        # Push is coming from a location where a marble exists, therefore the push is blocked.
        if self._spaces[push_coords[0]][push_coords[1]] is not None:
            return False

        return True

    def valid_end_position(self, coordinates, direction, player):
        """
        Given a location of a marble, a direction to push the marble, and a player, validates whether the ending
        position of the move is legal according to the rules of Kuba. Returns whether the ending position is valid.
        :param coordinates: Tuple (Int, Int), a location of a marble.
        :param direction: String, the direction to push the marble. 'L' = Left, 'R' = Right, 'F' = Forward, 'B' = Backward.
        :param player: Player object, the player making the move.
        :return: True or False, is the given starting position valid.
        """
        # Match the direction of the push to its momentum vector.
        momentum = self._moves[direction]

        # Apply the momentum vector to determine where the marble is being pushed to.
        end_coords = (coordinates[0]+momentum[0], coordinates[1]+momentum[1])

        # Continue applying the momentum vector until the marble is off the board or encounters an empty space.
        while self.is_on_board(end_coords) and self._spaces[end_coords[0]][end_coords[1]] is not None:
            end_coords = (end_coords[0] + momentum[0], end_coords[1] + momentum[1])

        # Capture the second to last spot of the final position. This is required in case we stay on the board and push
        # into an empty space.
        prev_spot = (end_coords[0]-momentum[0], end_coords[1]-momentum[1])

        # If the end position is on the board and the last marble seen matches the player's color, the move is invalid.
        if not self.is_on_board(end_coords) and self._spaces[prev_spot[0]][prev_spot[1]] == player.get_color():
            return False

        return True

    def move_marble(self, coordinates, direction, player):
        """
        Given a location of a marble, a direction to push the marble, and a player, updates the board state to reflect
        moving the marble.
        :param coordinates: Tuple (Int, Int), a location of a marble.
        :param direction: String, the direction to push the marble. 'L' = Left, 'R' = Right, 'F' = Forward, 'B' = Backward.
        :param player: Player object, the player making the move.
        :return: Nothing.
        """
        # TODO: Determine some way to calculate this once and share between validate and move functions
        # Match the direction of the push to its momentum vector.
        momentum = self._moves[direction]

        # Apply the momentum vector to determine where the marble is being pushed to.
        end_coords = (coordinates[0]+momentum[0], coordinates[1]+momentum[1])

        # Continue applying the momentum vector until the marble is off the board or encounters an empty space.
        while self.is_on_board(end_coords) and self._spaces[end_coords[0]][end_coords[1]] is not None:
            end_coords = (end_coords[0] + momentum[0], end_coords[1] + momentum[1])

        # Capture the second to last spot of the final position. This is required in case we stay on the board and push
        # into an empty space or we push off a marble.
        prev_spot = (end_coords[0]-momentum[0], end_coords[1]-momentum[1])

        # Capture any marbles that have fallen off.
        if not self.is_on_board(end_coords):
            player.add_captured_marble(self._spaces[prev_spot[0]][prev_spot[1]])
            end_coords = prev_spot

        # Go down the line from the end position to the start and move the marble locations.
        while end_coords != coordinates:
            next_spot = (end_coords[0]-momentum[0], end_coords[1]-momentum[1])
            self._spaces[end_coords[0]][end_coords[1]] = self._spaces[next_spot[0]][next_spot[1]]
            end_coords = next_spot

        # Set the starting location to empty.
        self._spaces[coordinates[0]][coordinates[1]] = None

    def return_marble(self, location):
        """
        Returns the marble at a given location.
        :param location: Tuple (Int, Int).
        :return: The marble at location, otherwise False if the location is off the board.
        """
        if self.is_on_board(location):
            return self._spaces[location[0]][location[1]]
        else:
            return False

    def has_won(self, current_player, next_player):
        """
        Determines whether the current player has won the game.
        :param current_player: Player object.
        :param next_player: Player object.
        :return: True or False, has the current player won the game.
        """
        # Current player has captured the requisite number of Red marbles to win.
        if current_player.get_captured_marbles() >= 7:
            return True

        # Determine whether the next player has any valid moves by checking every space on the board for their marbles.
        # For each marble found, check whether there are any valid ways to push the marble. If any exist, the game continues.
        for row_index, row in enumerate(self._spaces):
            for column_index, column in enumerate(row):
                if column == next_player.get_color():
                    for direction in self._moves.keys():
                        if self.validate_move((row_index, column_index), direction, next_player):
                            return False

        # No valid moves for next player, current player has won.
        return True

    def is_on_board(self, pos):
        """
        Returns whether a given location is on the board.
        :param pos: Tuple (Int, Int).
        :return: True or False, is pos on the board.
        """
        return (0 <= pos[0] <= 6) and (0 <= pos[1] <= 6)

    def get_marbles(self):
        """
        Returns a tuple of the count of each marble left on the game board.
        :return: Tuple (Int, Int, Int), the count of (W, B, R) marbles left on the board in that order.
        """
        W, B, R, = 0, 0, 0
        for row in self._spaces:
            for column in row:
                if column is not None:
                    if column == 'W':
                        W += 1
                    elif column == 'B':
                        B += 1
                    elif column == 'R':
                        R += 1

        return W, B, R


class KubaPlayer:
    """
    A representation of a Kuba Player. Maintains the state of the player, including their name, marble color, and number
    of captured marbles.
    """
    def __init__(self, player):
        """
        Initializes a new KubaPlayer.
        :param player: Tuple (String, String), the player's name and their marble color.
        """
        self._playername = player[0]
        self._color = player[1]
        self._captured_marbles = 0

    def get_playername(self):
        """
        Returns the player's name.
        :return: String, the player's name.
        """
        return self._playername

    def get_color(self):
        """
        Returns the player's marble color.
        :return: String, the player's marble color.
        """
        return self._color

    def get_captured_marbles(self):
        """
        Returns the number of Red marbles captured by the player.
        :return: Integer.
        """
        return self._captured_marbles

    def set_captured_marbles(self, quantity):
        """
        Sets the number of Red marbles captured by the player. For use in resetting captured marble count after Ko has
        occurred.
        :param quantity: Integer, the quantity to reset to.
        :return: Nothing.
        """
        self._captured_marbles = quantity

    def add_captured_marble(self, marble):
        """
        Increments the number of Red marbles captured by the player.
        :param marble: String, the marble being captured.
        :return: Nothing.
        """
        if marble == 'R':
            self._captured_marbles += 1


def main():
    print("Welcome to Kuba! The goal of this classic marble game is for two players to take turns trying to knock "
          "marbles off the game board.")
    print("To begin, please provide the names of each player.")
    print("Type 'q' at any time to quit.")
    print("Additional commands (parameters) include:")
    print("\tmove (playername, coordinates, direction)")
    print("\tturn")
    print("\twinner")
    print("\tcaptured (playername)")
    print("\tmarble (coordinates)")
    print("\tcount")
    name_one = input("Please provide the first player's name: ")
    name_two = input("Please provide the second player's name: ")
    game = KubaGame((name_one, 'W'), (name_two, 'B'))
    command = None
    while command != 'q' and game.get_winner() is None:
        command = input("Next command: ")
        if command == "move":
            name = input("Enter playername: ")
            if name != name_one and name != name_two:
                print("Invalid name.")
                continue
            row_coord = int(input("Enter row coordinate: "))
            col_coord = int(input("Enter column coordinate: "))
            coordinates = (row_coord, col_coord)
            direction = input("Enter direction as L, R, B, F: ")
            result = game.make_move(name, coordinates, direction)
            if result:
                print("Move recorded.")
            else:
                print("Invalid move.")
        elif command == "turn":
            print(game.get_current_turn())
        elif command == "winner":
            print(game.get_winner())
        elif command == "captured":
            name = input("Enter playername: ")
            print(game.get_captured(name))
        elif command == "marble":
            row_coord = int(input("Enter row coordinate: "))
            col_coord = int(input("Enter column coordinate: "))
            coordinates = (row_coord, col_coord)
            print(game.get_marble(coordinates))
        elif command == "count":
            print(game.get_marble_count())
        elif command == 'q':
            print("Goodbye!")
        else:
            print("Invalid command.")

    if game.get_winner():
        print(game.get_winner(), "has won!")



if __name__ == "__main__":
    main()
