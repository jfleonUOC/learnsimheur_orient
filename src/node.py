import math
from typing import List, Optional


def euclidean_distance(node1, node2):
    return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)
    

class Node:
    def __init__(self, id:int, x: float, y: float, score: float, isFirst: bool = False, isLast: bool = False):
        """
        Represents a node with coordinates (x, y) and a score.

        :param id: identifier of the node.
        :param x: X-coordinate of the node.
        :param y: Y-coordinate of the node.
        :param score: The score associated with the node.
        :param isFirst: True if the node is the first node in the sequence (optional, default is False).
        :param isLast: True if the node is the last node in the sequence (optional, default is False).
        """
        self.id = id
        self.x = x
        self.y = y
        self.score = score
        self.isFirst = isFirst
        self.isLast = isLast

    def __str__(self) -> str:
        return f"Node {self.id}"

    def __repr__(self) -> str:
        return f"Node {self.id}"
