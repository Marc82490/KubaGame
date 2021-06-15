# Author: Marc Zalik
# Date: 2021-05-20
# Description: Unit tests for Kuba Game.

import unittest
from KubaGame import KubaGame, KubaBoard


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))

    def test_init_game(self):
        result = list()
        result.append(self.game._turn)
        result.append(self.game._winner)
        result.append(self.game._captured_marbles)
        result.append(self.game._player_1_prev_board_state)
        result.append(self.game._player_1_prev_player_state)
        result.append(self.game._player_2_prev_board_state)
        result.append(self.game._player_2_prev_player_state)
        self.assertEqual(result, [None, None, {}, None, None, None, None])

    def test_first_make_move(self):
        self.game.make_move('PlayerA', (6, 5), 'F')
        board = self.game._board.get_state()
        self.assertEqual(self.game.get_current_turn(), 'PlayerB')
        self.assertEqual(board, [['W', 'W', None, None, None, 'B', 'B'], ['W', 'W', None, 'R', None, 'B', 'B'],
                                 [None, None, 'R', 'R', 'R', None, None], [None, 'R', 'R', 'R', 'R', 'R', None],
                                 [None, None, 'R', 'R', 'R', 'W', None], ['B', 'B', None, 'R', None, 'W', 'W'],
                                 ['B', 'B', None, None, None, None, 'W']])

    def test_second_make_move(self):
        self.game.make_move('PlayerA', (6, 5), 'F')
        self.game.make_move('PlayerB', (0, 5), 'B')
        board = self.game._board.get_state()
        self.assertEqual(self.game.get_current_turn(), 'PlayerA')
        self.assertEqual(board, [['W', 'W', None, None, None, None, 'B'], ['W', 'W', None, 'R', None, 'B', 'B'],
                                 [None, None, 'R', 'R', 'R', 'B', None], [None, 'R', 'R', 'R', 'R', 'R', None],
                                 [None, None, 'R', 'R', 'R', 'W', None], ['B', 'B', None, 'R', None, 'W', 'W'],
                                 ['B', 'B', None, None, None, None, 'W']])

    def test_invalid_coordinates(self):
        response = self.game.make_move('PlayerA', (10, 10), 'F')
        board = self.game._board.get_state()
        self.assertEqual(response, False)
        self.assertEqual(board, [['W', 'W', None, None, None, 'B', 'B'], ['W', 'W', None, 'R', None, 'B', 'B'],
                                 [None, None, 'R', 'R', 'R', None, None], [None, 'R', 'R', 'R', 'R', 'R', None],
                                 [None, None, 'R', 'R', 'R', None, None], ['B', 'B', None, 'R', None, 'W', 'W'],
                                 ['B', 'B', None, None, None, 'W', 'W']])

    def test_no_double_moves(self):
        self.game.make_move('PlayerA', (6, 5), 'F')
        self.game.make_move('PlayerA', (6, 6), 'L')
        board = self.game._board.get_state()
        self.assertEqual(self.game.get_current_turn(), 'PlayerB')
        self.assertEqual(board, [['W', 'W', None, None, None, 'B', 'B'], ['W', 'W', None, 'R', None, 'B', 'B'],
                                 [None, None, 'R', 'R', 'R', None, None], [None, 'R', 'R', 'R', 'R', 'R', None],
                                 [None, None, 'R', 'R', 'R', 'W', None], ['B', 'B', None, 'R', None, 'W', 'W'],
                                 ['B', 'B', None, None, None, None, 'W']])

    def test_ko(self):
        self.game.make_move('PlayerA', (6, 5), 'F')
        self.game.make_move('PlayerB', (0, 5), 'B')
        self.game.make_move('PlayerA', (5, 5), 'F')
        board_one = self.game._board.get_state()
        self.game.make_move('PlayerB', (0, 5), 'B')
        board_two = self.game._board.get_state()
        self.assertEqual(self.game.get_current_turn(), 'PlayerB')
        self.assertEqual(board_one, board_two)
        self.assertEqual(board_two, [['W', 'W', None, None, None, 'B', 'B'], ['W', 'W', None, 'R', None, 'B', 'B'],
                                 [None, None, 'R', 'R', 'R', 'R', None], [None, 'R', 'R', 'R', 'R', 'W', None],
                                 [None, None, 'R', 'R', 'R', 'W', None], ['B', 'B', None, 'R', None, None, 'W'],
                                 ['B', 'B', None, None, None, None, 'W']])

    def test_move_wrong_color(self):
        result = self.game.make_move('PlayerA', (0, 5), 'B')
        self.assertEqual(result, False)
        self.assertEqual(self.game._turn, None)

    def test_any_player_start(self):
        result = self.game.make_move('PlayerB', (0, 5), 'B')
        self.assertEqual(result, True)
        self.assertEqual(self.game._turn, 0)

    def test_blocked_push(self):
        result = self.game.make_move('PlayerA', (5, 5), 'F')
        self.assertEqual(result, False)

    def test_push_own_marble_off(self):
        board_one = self.game._board.get_state()
        self.game.make_move('PlayerA', (6,5), 'R')
        board_two = self.game._board.get_state()
        self.assertEqual(board_one, board_two)
        self.assertEqual(board_two, [['W', 'W', None, None, None, 'B', 'B'], ['W', 'W', None, 'R', None, 'B', 'B'],
                                 [None, None, 'R', 'R', 'R', None, None], [None, 'R', 'R', 'R', 'R', 'R', None],
                                 [None, None, 'R', 'R', 'R', None, None], ['B', 'B', None, 'R', None, 'W', 'W'],
                                 ['B', 'B', None, None, None, 'W', 'W']])

    def test_update_turn_only_after_success_1(self):
        self.game.make_move('PlayerA', (5, 5), 'F')
        self.assertEqual(self.game.get_current_turn(), None)

    def test_update_turn_only_after_success_2(self):
        self.game.make_move('PlayerB', (0, 5), 'B')
        self.assertEqual(self.game.get_current_turn(), 'PlayerA')
        self.game.make_move('PlayerA', (5, 5), 'F')
        self.assertEqual(self.game.get_current_turn(), 'PlayerA')

    def test_get_winner_1(self):
        """
        Check for winner by marble count.
        """
        self.game.make_move('PlayerA', (1, 0), 'R')
        self.game.make_move('PlayerB', (0, 6), 'B')
        self.game.make_move('PlayerA', (1, 1), 'R')
        self.game.make_move('PlayerB', (1, 6), 'B')
        self.game.make_move('PlayerA', (1, 3), 'B')
        self.game.make_move('PlayerB', (2, 6), 'B')
        self.game.make_move('PlayerA', (2, 3), 'B')
        self.game.make_move('PlayerB', (3, 6), 'B')
        self.game.make_move('PlayerA', (3, 3), 'B')
        self.game.make_move('PlayerB', (4, 6), 'B')
        self.game.make_move('PlayerA', (4, 3), 'B')
        self.game.make_move('PlayerB', (6, 0), 'F')
        self.game.make_move('PlayerA', (5, 3), 'B')
        self.game.make_move('PlayerB', (5, 0), 'F')
        self.game.make_move('PlayerA', (1, 2), 'B')
        self.game.make_move('PlayerB', (4, 0), 'F')
        self.game.make_move('PlayerA', (2, 2), 'B')
        self.game.make_move('PlayerB', (3, 0), 'F')
        self.game.make_move('PlayerA', (3, 2), 'B')
        self.game.make_move('PlayerB', (2, 0), 'F')
        self.game.make_move('PlayerA', (4, 2), 'B')
        self.game.make_move('PlayerB', (0, 0), 'R')
        self.game.make_move('PlayerA', (5, 2), 'B')
        winner = self.game.get_winner()
        self.assertEqual(winner, "PlayerA")

    def test_get_winner_2(self):
        """
        Check for winner by no legal moves.
        """
        self.game.make_move('PlayerA', (6, 5), 'F')
        self.game.make_move('PlayerB', (0, 5), 'B')
        self.game.make_move('PlayerA', (5, 5), 'F')
        self.game.make_move('PlayerB', (5, 0), 'R')
        self.game.make_move('PlayerA', (4, 5), 'F')
        self.game.make_move('PlayerB', (5, 1), 'R')
        self.game.make_move('PlayerA', (3, 5), 'F')
        self.game.make_move('PlayerB', (5, 2), 'R')
        self.game.make_move('PlayerA', (2, 5), 'F')
        self.game.make_move('PlayerB', (5, 3), 'R')
        self.game.make_move('PlayerA', (0, 1), 'B')
        self.game.make_move('PlayerB', (5, 4), 'R')
        self.game.make_move('PlayerA', (1, 1), 'B')
        self.game.make_move('PlayerB', (5, 6), 'B')
        self.game.make_move('PlayerA', (2, 1), 'B')
        self.game.make_move('PlayerB', (5, 5), 'F')
        self.game.make_move('PlayerA', (3, 1), 'B')
        self.game.make_move('PlayerB', (4, 5), 'L')
        self.game.make_move('PlayerA', (4, 0), 'B')
        self.game.make_move('PlayerB', (4, 4), 'L')
        self.game.make_move('PlayerA', (0, 5), 'R')
        self.game.make_move('PlayerB', (4, 3), 'L')
        self.game.make_move('PlayerA', (5, 0), 'F')
        self.game.make_move('PlayerA', (1, 5), 'R')
        self.game.make_move('PlayerB', (4, 2), 'L')
        self.game.make_move('PlayerA', (0, 0), 'B')
        self.game.make_move('PlayerB', (4, 1), 'L')
        self.game.make_move('PlayerA', (1, 0), 'B')
        self.game.make_move('PlayerB', (4, 0), 'R')
        self.game.make_move('PlayerA', (5, 0), 'B')
        self.game.make_move('PlayerB', (4, 1), 'R')
        self.game.make_move('PlayerA', (3, 0), 'R')
        self.game.make_move('PlayerB', (4, 2), 'F')
        self.game.make_move('PlayerA', (3, 1), 'R')
        self.game.make_move('PlayerB', (3, 3), 'F')
        self.game.make_move('PlayerA', (3, 2), 'R')
        self.game.make_move('PlayerB', (6, 6), 'L')
        self.game.make_move('PlayerA', (5, 1), 'R')
        self.game.make_move('PlayerB', (6, 5), 'L')
        self.game.make_move('PlayerA', (5, 2), 'R')
        self.game.make_move('PlayerC', (5, 3), 'B')
        self.game.make_move('PlayerB', (6, 4), 'L')
        self.game.make_move('PlayerA', (5, 3), 'B')
        winner = self.game.get_winner()
        self.assertEqual(winner, "PlayerA")

    def test_no_moves_after_win(self):
        self.game.make_move('PlayerA', (1, 0), 'R')
        self.game.make_move('PlayerB', (0, 6), 'B')
        self.game.make_move('PlayerA', (1, 1), 'R')
        self.game.make_move('PlayerB', (1, 6), 'B')
        self.game.make_move('PlayerA', (1, 3), 'B')
        self.game.make_move('PlayerB', (2, 6), 'B')
        self.game.make_move('PlayerA', (2, 3), 'B')
        self.game.make_move('PlayerB', (3, 6), 'B')
        self.game.make_move('PlayerA', (3, 3), 'B')
        self.game.make_move('PlayerB', (4, 6), 'B')
        self.game.make_move('PlayerA', (4, 3), 'B')
        self.game.make_move('PlayerB', (6, 0), 'F')
        self.game.make_move('PlayerA', (5, 3), 'B')
        self.game.make_move('PlayerB', (5, 0), 'F')
        self.game.make_move('PlayerA', (1, 2), 'B')
        self.game.make_move('PlayerB', (4, 0), 'F')
        self.game.make_move('PlayerA', (2, 2), 'B')
        self.game.make_move('PlayerB', (3, 0), 'F')
        self.game.make_move('PlayerA', (3, 2), 'B')
        self.game.make_move('PlayerB', (2, 0), 'F')
        self.game.make_move('PlayerA', (4, 2), 'B')
        self.game.make_move('PlayerB', (0, 0), 'R')
        self.game.make_move('PlayerA', (5, 2), 'B')
        result = self.game.make_move('PlayerB', (0, 1), 'R')
        self.assertEqual(result, False)

    def test_get_captured_1(self):
        """
        Test captured marbles at initialization.
        """
        captured_one = self.game.get_captured('PlayerA')
        captured_two = self.game.get_captured('PlayerB')
        self.assertEqual(captured_one, 0)
        self.assertEqual(captured_two, 0)

    def test_get_captured_2(self):
        """
        Test captured after knocking off other player's marble.
        """
        self.game.make_move('PlayerA', (6, 5), 'F')
        self.game.make_move('PlayerB', (0, 5), 'B')
        self.game.make_move('PlayerA', (5, 5), 'F')
        self.game.make_move('PlayerB', (5, 0), 'R')
        self.game.make_move('PlayerA', (4, 5), 'F')
        captured_one = self.game.get_captured('PlayerA')
        captured_two = self.game.get_captured('PlayerB')
        self.assertEqual(captured_one, 0)
        self.assertEqual(captured_two, 0)

    def test_get_captured_3(self):
        """
        Test captured after knocking off neutral marble.
        """
        self.game.make_move('PlayerA', (6, 5), 'F')
        self.game.make_move('PlayerB', (0, 5), 'B')
        self.game.make_move('PlayerA', (5, 5), 'F')
        self.game.make_move('PlayerB', (5, 0), 'R')
        self.game.make_move('PlayerA', (4, 5), 'F')
        self.game.make_move('PlayerB', (5, 1), 'R')
        self.game.make_move('PlayerA', (3, 5), 'F')
        self.game.make_move('PlayerB', (5, 2), 'R')
        self.game.make_move('PlayerA', (2, 5), 'F')
        captured_one = self.game.get_captured('PlayerA')
        captured_two = self.game.get_captured('PlayerB')
        self.assertEqual(captured_one, 1)
        self.assertEqual(captured_two, 0)

    def test_get_marble_1(self):
        """
        Test for valid marble.
        """
        marble = self.game.get_marble((0,0))
        self.assertEqual(marble, 'W')

    def test_get_marble_2(self):
        """
        Test for marble at empty space.
        """
        marble = self.game.get_marble((3,0))
        self.assertEqual(marble, 'X')

    def test_marble_count_1(self):
        """
        Test marble count at initialization.
        """
        count = self.game.get_marble_count()
        self.assertEqual(count, (8, 8, 13))

    def test_marble_count_2(self):
        """
        Test marble count after knocking off other player's marble.
        """
        self.game.make_move('PlayerA', (6, 5), 'F')
        self.game.make_move('PlayerB', (0, 5), 'B')
        self.game.make_move('PlayerA', (5, 5), 'F')
        self.game.make_move('PlayerB', (5, 0), 'R')
        self.game.make_move('PlayerA', (4, 5), 'F')
        count = self.game.get_marble_count()
        self.assertEqual(count, (8, 7, 13))

    def test_marble_count_3(self):
        """
        Test marble count after knocking off neutral marble.
        """
        self.game.make_move('PlayerA', (6, 5), 'F')
        self.game.make_move('PlayerB', (0, 5), 'B')
        self.game.make_move('PlayerA', (5, 5), 'F')
        self.game.make_move('PlayerB', (5, 0), 'R')
        self.game.make_move('PlayerA', (4, 5), 'F')
        self.game.make_move('PlayerB', (5, 1), 'R')
        self.game.make_move('PlayerA', (3, 5), 'F')
        self.game.make_move('PlayerB', (5, 2), 'R')
        self.game.make_move('PlayerA', (2, 5), 'F')
        count = self.game.get_marble_count()
        self.assertEqual(count, (8, 6, 12))


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))

    def test_new_board(self):
        board = self.game._board.get_state()
        self.assertEqual(board, [['W', 'W', None, None, None, 'B', 'B'], ['W', 'W', None, 'R', None, 'B', 'B'],
                                     [None, None, 'R', 'R', 'R', None, None], [None, 'R', 'R', 'R', 'R', 'R', None],
                                     [None, None, 'R', 'R', 'R', None, None], ['B', 'B', None, 'R', None, 'W', 'W'],
                                     ['B', 'B', None, None, None, 'W', 'W']])


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.game = KubaGame(('PlayerA', 'W'), ('PlayerB', 'B'))

    def test_new_players(self):
        name_one = self.game._player_1.get_playername()
        color_one = self.game._player_1.get_color()
        name_two = self.game._player_2.get_playername()
        color_two = self.game._player_2.get_color()
        self.assertEqual(name_one, 'PlayerA')
        self.assertEqual(name_two, 'PlayerB')
        self.assertEqual(color_one, 'W')
        self.assertEqual(color_two, 'B')

    def test_get_captured_marbles_1(self):
        """
        Check count at initialization.
        """
        captured_one = self.game._player_1.get_captured_marbles()
        captured_two = self.game._player_2.get_captured_marbles()
        self.assertEqual(captured_one, 0)
        self.assertEqual(captured_two, 0)

    def test_get_captured_marbles_2(self):
        """
        Check count after knocking off other player's marble.
        """
        self.game.make_move('PlayerA', (6, 5), 'F')
        self.game.make_move('PlayerB', (0, 5), 'B')
        self.game.make_move('PlayerA', (5, 5), 'F')
        self.game.make_move('PlayerB', (5, 0), 'R')
        self.game.make_move('PlayerA', (4, 5), 'F')
        captured_one = self.game._player_1.get_captured_marbles()
        captured_two = self.game._player_2.get_captured_marbles()
        self.assertEqual(captured_one, 0)
        self.assertEqual(captured_two, 0)

    def test_get_captured_marbles_3(self):
        """
        Check count after knocking off neutral marble.
        """
        self.game.make_move('PlayerA', (6, 5), 'F')
        self.game.make_move('PlayerB', (0, 5), 'B')
        self.game.make_move('PlayerA', (5, 5), 'F')
        self.game.make_move('PlayerB', (5, 0), 'R')
        self.game.make_move('PlayerA', (4, 5), 'F')
        self.game.make_move('PlayerB', (5, 1), 'R')
        self.game.make_move('PlayerA', (3, 5), 'F')
        self.game.make_move('PlayerB', (5, 2), 'R')
        self.game.make_move('PlayerA', (2, 5), 'F')
        captured_one = self.game._player_1.get_captured_marbles()
        captured_two = self.game._player_2.get_captured_marbles()
        self.assertEqual(captured_one, 1)
        self.assertEqual(captured_two, 0)


if __name__ == "__main__":
    unittest.main()
