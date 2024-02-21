from typing import Dict, List
from enum import Enum

import h3

class Game:
    pass



class HexState(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2
    EMPTY    = 0

class Region:
    """ConvexRegion Class 
    """
    def __init__(self,hexagon_list:List[str]):
        if not self.is_region(hexagon_list):
            raise ValueError("the list doesn't represent a convex region")
        self.hexagons = hexagon_list

    @staticmethod
    def is_region(hexagon_list:list[str]):
        visited = set()
        queue = [hexagon_list[0]]

        while queue:
            current_hexagon = queue.pop(0)
            if current_hexagon in visited:
                continue
            visited.add(current_hexagon)
            neighbors = h3.k_ring(current_hexagon,  1)  # Find  1-degree neighbors
            # Only add neighbors to the queue if they are in the original list
            queue.extend(neighbor for neighbor in neighbors if neighbor in hexagon_list)

        return len(visited) == len(hexagon_list)


class NonEmptyHexError(Exception):
    pass

class Board:
    hexagons:List[str]
    state: Dict[str, HexState]

    def __init__(self, lat, lng, size, res:int=6):
            # Generate initial set of hexagons using k-rings
            center_hex = h3.geo_to_h3(lat, lng, res)
            hexagons = h3.k_ring(center_hex, size)
            
            # Remove hexagons from the border until we have the required size
            while len(hexagons) > size:
                border_hex = hexagons.pop(0)
                neighbors = h3.k_ring(border_hex, 1)
                if all(neighbor in hexagons for neighbor in neighbors):
                    hexagons.append(border_hex)
            
            # Store the hexagons as the board
            self.hexagons = hexagons
    
    def empty_hex(self) -> list[str]:
        empty_hexagons = list(filter(lambda hexagon: self.state[hexagon] == HexState.EMPTY, self.hexagons))
        return empty_hexagons
    
    def plot(self):
        pass 

    def take(self, hex:str, player:int):
        if self.state[hex] == HexState.EMPTY:
            self.state[hex] = HexState(player)
        else:
            raise NonEmptyHexError("Hexagon is not empty")
    
    def get_regions(player:int) -> List[Region]:
        pass

    @property
    def is_finished(self) -> bool:
        return len(self.empty_hex) == 0
    
