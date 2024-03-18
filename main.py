from players import RandomPlayer
from hexi import Board, Game


# Create two RandomPlayer instances
player1 = RandomPlayer("Player 1", 1)
player2 = RandomPlayer("Player 2", 2)

# Generate a random board
board = Board.generate_random(10, 0, 0, 1)

# Create a game with the two players and the board
game = Game(board, player1, player2)

# Play the game
game.play()
