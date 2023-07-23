from typing import List, Union

from node import Node, euclidean_distance


class Arc:
    ''' A class defining Arc objects '''

    def __init__(self, start: Node, end: Node) -> None:
        """
        Initialize an Arc object.

        Parameters:
            start (Node): The start node of the edge (arc).
            end (Node): The end node of the edge (arc).
        """
        self.start: Node = start  # start node of the edge (arc)
        self.end: Node = end  # end node of the edge (arc)
        self.cost: float = 0.0  # edge cost (e.g., travel time, monetary cost, etc.)
        self.savings: float = 0.0  # edge savings (Clarke & Wright)
        self.efficiency: float = 0.0  # edge efficiency (enriched savings)

        self.calc_cost()

    def calc_cost(self):
        self.cost = euclidean_distance(self.start, self.end)
        return self.cost 

    def __str__(self) -> str:
        return f"Arc {self.start.id}-{self.end.id}"

    def __repr__(self) -> str:
        return f"Arc {self.start.id}-{self.end.id}"