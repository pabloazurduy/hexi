from typing import List, Dict, Protocol, Set, Optional
from collections import UserDict
from enum import Enum
from dataclasses import dataclass
from copy import deepcopy
import random

import h3
import matplotlib.pyplot as plt

class PlayerID(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2

@dataclass 
class Hex:
    id:str 
    state:Optional[PlayerID]=None
    value:int = 1

@dataclass
class BoardState(UserDict):
    data:Dict[str,Hex]

    @classmethod
    def from_list(cls, hexagons:List[hex]):
        return cls(data = {h.id: h for h in hexagons})
    
    @property
    def hexagons(self) -> List[PlayerID]:
        return list(self.data.values())
    
    @property
    def hexagons_available(self) ->List[str]:
        return [hid for hid in self.data.keys() if self.data[hid].state is None ]

    @property
    def is_finished(self) -> bool:
        return all(hex.state is not None for hex in self.hexagons)

    def hex_empty(self, hex_id:str) -> bool:
        return self.data[hex_id].state is None
class NotValidPlay(Exception):
    pass
@dataclass
class Board:
    states: List[BoardState]

    @classmethod
    def generate_random(cls, size: int, lat: float, long: float, hexagon_resolution: int):
        origin_hex_id = h3.geo_to_h3(lat, long, hexagon_resolution)
        origin_hex = Hex(id=origin_hex_id, state=None)
        
        hex_ids: List[str] = [origin_hex.id]
        idx:int = 0
        while len(hex_ids) < size:
            current_hex = hex_ids[idx]
            candidates = h3.k_ring(current_hex, 1)-set(hex_ids)
            hex_ids.extend(random.sample(sorted(candidates), min(size-len(hex_ids), len(candidates))))
            idx+=1
        hexagons = [Hex(id=hid, state=None) for hid in hex_ids]

        return cls([BoardState.from_list(hexagons=hexagons)])
    
    @property
    def last_state(self) -> BoardState:
        return self.states[-1]

    def play_take(self, hex_id: str, player:PlayerID):
        if self.last_state.hex_empty(hex_id):
            new_state = deepcopy(self.last_state)
            new_state[hex_id].state = player 
            self.states.append(BoardState(new_state))
        else:
            raise NotValidPlay(f'hexagon {hex_id} already taken {new_state[hex_id].state = }')
  
    
    def plot_last_state(self):
        self.plot_state(self.last_state)

    @staticmethod
    def plot_state(state: BoardState):
        for hex_id, hex_state in state.hexagons.dict:
            boundary = h3.h3_to_geo_boundary(hex_id, geo_json=True)
            plt.fill(boundary[0], boundary[1], color='blue' if hex_state == PlayerID.PLAYER_1 else 'red')
        plt.show()

    def make_gif(self):
        # Implementation for creating a GIF from all states
        raise NotImplementedError


    @property
    def is_finished(self):
        return self.last_state.is_finished

class Player(Protocol):
    name: str
    id: PlayerID

    def next_play(self, board: Board) -> str:
        pass

@dataclass
class Game:
    def __init__(self, board: Board, player1: Player, player2: Player):
        self.board = board
        self.player1 = player1
        self.player2 = player2

    def play(self):
        while not self.board.is_finished:
            player = random.choice([self.player1, self.player2])
            hex_id = player.next_play(self.board)
            self.board.play_take(hex_id, player=player.id)
