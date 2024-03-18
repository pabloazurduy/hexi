import pytest
from hexi import Board, BoardState, Player, Game, PlayerID

class TestBoard:
    @pytest.mark.parametrize("size", [5, 10000, 1])
    def test_generate_random(self, size):
        board = Board.generate_random(size, 0, 0, 8)
        assert len(board.last_state.hexagons) == size

    def test_take(self):
        board = Board.generate_random(5, 0, 0, 1)
        hex_id = board.last_state.hexagons[0].id
        board.play_take(hex_id, PlayerID.PLAYER_1)
        assert board.last_state[hex_id].state != None

    def test_is_finished(self):
        board = Board.generate_random(5, 0, 0, 1)
        assert not board.is_finished
        for hex_id in board.last_state.keys():
            board.play_take(hex_id, PlayerID.PLAYER_1)
        assert board.is_finished

class TestPlayer:
    class MockPlayer(Player):
        def __init__(self, name, id):
            self.name = name
            self.id = id

        def next_play(self, board):
            return board.last_state.hexagons_available[0]

    def test_next_play(self):
        player = self.MockPlayer("Test Player", 1)
        board = Board.generate_random(5, 0, 0, 1)
        hex_id = player.next_play(board)
        assert hex_id in board.last_state.keys()

class TestGame:
    class MockPlayer:
        def __init__(self, name, id):
            self.name = name
            self.id = id

        def next_play(self, board):
            return board.last_state.hexagons_available[0]

    def test_game_play(self):
        player1 = self.MockPlayer("Player 1", PlayerID.PLAYER_1)
        player2 = self.MockPlayer("Player 2", PlayerID.PLAYER_2)
        board = Board.generate_random(5, 0, 0, 1)
        game = Game(board, player1, player2)
        game.play()
        assert board.is_finished
