import math
from typing import List, Optional


def euclidean_distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)
    

class Node:
    def __init__(self, id:int, x: float, y: float, reward: float, is_start: bool = False, is_end: bool = False):
        """
        Represents a node with coordinates (x, y) and a reward.

        :param id: identifier of the node.
        :param x: X-coordinate of the node.
        :param y: Y-coordinate of the node.
        :param reward: The reward associated with the node.
        :param is_start: True if the node is the first node (start depot).
        :param is_end: True if the node is the last node (end depot).
        """
        self.id = id
        self.x = x
        self.y = y
        self.reward = reward
        self.is_start = is_start
        self.is_end = is_end

    def __str__(self) -> str:
        return f"Node {self.id}"

    def __repr__(self) -> str:
        return f"Node {self.id}"
    