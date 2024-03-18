import random
from hexi import Board, Player

class RandomPlayer(Player):
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id

    def next_play(self, board: Board) -> str:
        # Find all hexagons that are not owned (NULL state)
        if board.last_state.hexagons_available:
            # Select a random hexagon from the list of free hexagons
            return random.choice(board.last_state.hexagons_available)
        else:
            # If there are no free hexagons, return None or handle this case as needed
            return None
