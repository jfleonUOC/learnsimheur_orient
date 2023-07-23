from typing import List

from arc import Arc

class Route:
    ''' A class defining Route objects '''

    def __init__(self) -> None:
        """
        Initialize a Route object.

        Attributes:
            edges (List[Arc]): A list of sorted edges/arcs in this route.
            cost (float): The cost of this route.
            reward (float): The total reward collected in this route.
        """
        self.arcs: List[Arc] = []  # sorted arcs in this route
        self.cost: float = 0.0  # cost of this route
        self.reward: float = 0.0  # total reward collected in this route

    def add_arc(self, new_arc):
        self.arcs.append(new_arc)
        self.compute_cost()
        self.compute_reward()

    def remove_arc(self, new_arc):
        self.arcs.remove(new_arc)
        self.compute_cost()
        self.compute_reward()
    
    def compute_cost(self):
        self.cost = 0.0 # reset
        for arc in self.arcs:
            # print(f"{arc} -->> cost={arc.cost}")
            self.cost += arc.cost
        # print(f"!!{self.cost =}")
        return self.cost

    def compute_reward(self):
        self.reward = 0.0 # reset
        for arc in self.arcs:
            self.reward += arc.end.reward
        return self.reward

    def compile_route_name(self):
        route_name = f"Route {self.arcs[0].start.id}-"
        for arc in self.arcs[:-1]:
            route_name += f"{arc.end.id}-"
        route_name += f"{self.arcs[-1].end.id}"
        return route_name

    def __str__(self) -> str:
        return self.compile_route_name()

    def __repr__(self) -> str:
        return self.compile_route_name()

    def is_linked_to_start(self, node):
        for arc in self.arcs:
            if arc.end == node and arc.start.is_start:
                return True
        return False

    def is_linked_to_end(self, node):
        for arc in self.arcs:
            if arc.start == node and arc.end.is_end:
                return True
        return False

    #TODO: implement check for route: is the sequence of nodes/arcs correct?

# if __name__ == "__main__":