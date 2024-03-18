import random
from hexi import Board, Player, HexState

class RandomPlayer(Player):
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id

    def next_play(self, board: Board) -> str:
        # Find all hexagons that are not owned (NULL state)
        free_hexagons = [hex_id for hex_id, hex_state in board.states[-1].state.items() if hex_state == HexState.NULL]
        if free_hexagons:
            # Select a random hexagon from the list of free hexagons
            return random.choice(free_hexagons)
        else:
            # If there are no free hexagons, return None or handle this case as needed
            return None
