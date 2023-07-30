from typing import List, Dict, Union
import math
import random

from node import Node, euclidean_distance
from importer import Importer
from efficiencylist import EfficiencyList
from heuristic import pj_heuristic


class Emulation:
    def __init__(self, nodes: List[Node], max_cost:float):
        """
        Represents the Emulation class that takes the network of nodes as input.

        Args:
            nodes (List[Node]): List of Node instances.
        """
        self.nodes = nodes
        self.max_cost = max_cost
        self.current_node: Node = next((node for node in self.nodes if node.id == 0), None)
        self.path_covered: List[Node] = [self.current_node]
        self.current_reward: float = 0.0
        self.current_cost: float = 0.0
        self.static_cost: float = 0.0

    def get_current_state(self) -> Dict:
        """
        Provides the current state information of the Emulation.

        Returns:
            Dict: A dictionary containing the current state information.
        """
        return {
            "current_node": self.current_node,
            "path_covered": self.path_covered,
            "current_reward": self.current_reward,
            "current_cost": self.current_cost,
            "static_cost": self.static_cost
        }
    
    def get_initial_conditions(self):

        return {
            "initial_max_cost": self.max_cost,
            "num_nodes": len(self.nodes)
        }

    def step(self, new_node_id: int) -> None:
        """
        Selects a new node from the list of nodes and moves to that node.
        The reward and cost are recalculated, and the current node is added to the path covered.

        Args:
            new_node_id (int): The id of the new node to move to.
        
        Raises:
            ValueError: If the provided new_node_id does not match any node in the list of nodes.
        """
        # Find the node with the given id in the list of nodes
        new_node = next((node for node in self.nodes if node.id == new_node_id), None)

        if new_node is None:
            raise ValueError("Invalid node id provided")

        if self.current_node is not None:
            # Calculate the distance between the current node and the new node
            distance_static = euclidean_distance(self.current_node, new_node)
            params = dynamic_param()
            dynamic_component = dynamic_function(params, len(self.path_covered))
            distance_dynamic = distance_static + dynamic_component
            print(f"{distance_static = }")
            print(f"{distance_dynamic = }")

            # Update the current cost with the calculated distance
            self.current_cost += distance_dynamic
            self.static_cost += distance_static

            # Update the current reward with the new node's score
            self.current_reward += new_node.reward
        else:
            raise ReferenceError("Current Node not provided")

        # Move to the new node
        self.current_node = new_node

        # Add the new node to the path covered
        self.path_covered.append(self.current_node)
    
    #TODO: verify that the solution is still feasible

def dynamic_param(param_seed:int=1, n_param:int=4):
    """
    Generate dynamic parameters
    By default consider 4 parameters for the function:
    1. trafic
    2. weather
    3. day of the week
    4. state of charge
    (5. driver experience)
    """
    params = []
    random.seed(param_seed)
    for i in range(n_param):
        params.append(random.random())
    return params

def dynamic_function(parameters, tstep, variability:int=1):
    #TODO: add the start-end nodes as part of the dynamic_function?
    deltas = []
    for p in parameters:
        delta_i = variability*math.sin((tstep*(math.pi)*p))
        deltas.append(delta_i)
    delta_total = sum(deltas)
    return delta_total

if __name__ == "__main__":
    # Import files
    # file_path = "input/ref/set_64_1/set_64_1_15.txt"
    file_path = "input/ref/Tsiligirides 3/tsiligirides_problem_3_budget_070.txt"
    importer = Importer(file_path)
    importer.print_nodes()
    nodes = importer.node_data
    routeMaxCost = importer.Tmax

    # Generate efficiency list
    eff_list = EfficiencyList(nodes)
    eff_list.generate(alpha=0.5)

    # Run PJ Heuristic
    merged_sol = pj_heuristic(nodes, eff_list, routeMaxCost, useBR=True, verbose=False)
    listOfNodes = merged_sol.get_best_route().get_nodes()
    print(listOfNodes)

    # Create an instance of the Emulation class
    emulator = Emulation(nodes)

    # Get the current state
    print(emulator.get_current_state())

    # Move to nodes and update the current state
    # emulator.step(2)
    # emulator.step(10)
    # print(emulator.get_current_state())
    # print(emulator.get_current_state()["path_covered"])
    for position in listOfNodes[1:]:
        emulator.step(position)
        print(emulator.get_current_state())
