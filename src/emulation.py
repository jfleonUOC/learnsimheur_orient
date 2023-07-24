from typing import List, Dict, Union
import math

from node import Node, euclidean_distance
from importer import Importer
from efficiencylist import EfficiencyList
from heuristic import pj_heuristic


class Emulation:
    def __init__(self, nodes: List[Node]):
        """
        Represents the Emulation class that takes the network of nodes as input.

        Args:
            nodes (List[Node]): List of Node instances.
        """
        self.nodes = nodes
        self.current_node: Node = next((node for node in self.nodes if node.id == 0), None)
        self.path_covered: List[Node] = [self.current_node]
        self.current_reward: float = 0.0
        self.current_cost: float = 0.0

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
            "current_cost": self.current_cost
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
            distance = euclidean_distance(self.current_node, new_node)
            #TODO: create random generator of conditions x1, x2, x3, x4
            dynamic_component = dynamic_function(x_1, x_2, x_3, x_4, len(self.path_covered))
            distance += dynamic_component
            # print(f"{distance = }")

            # Update the current cost with the calculated distance
            self.current_cost += distance

            # Update the current reward with the new node's score
            self.current_reward += new_node.reward
        else:
            raise ReferenceError("Current Node not provided")

        # Move to the new node
        self.current_node = new_node

        # Add the new node to the path covered
        self.path_covered.append(self.current_node)

def dynamic_function(x_1, x_2, x_3, x_4, tstep):
    delta_x_1 = math.sin(tstep*x_1)
    delta_x_2 = math.sin(tstep*x_2)
    delta_x_3 = math.sin(tstep*x_3)
    delta_x_4 = math.sin(tstep*x_4)
    delta = delta_x_1 + delta_x_2 + delta_x_3 + delta_x_4
    return delta

if __name__ == "__main__":
    # # Import files
    # # file_path = "input/ref/set_64_1/set_64_1_15.txt"
    # file_path = "input/ref/Tsiligirides 3/tsiligirides_problem_3_budget_070.txt"
    # importer = Importer(file_path)
    # importer.print_nodes()
    # nodes = importer.node_data
    # routeMaxCost = importer.Tmax

    # # Generate efficiency list
    # eff_list = EfficiencyList(nodes)
    # eff_list.generate(alpha=0.5)

    # # Run PJ Heuristic
    # merged_sol = pj_heuristic(nodes, eff_list, routeMaxCost, useBR=True, verbose=False)
    # listOfNodes = merged_sol.get_best_route().get_nodes()
    # print(listOfNodes)

    # # Create an instance of the Emulation class
    # emulator = Emulation(nodes)

    # # Get the current state
    # print(emulator.get_current_state())

    # # Move to nodes and update the current state
    # # emulator.step(2)
    # # emulator.step(10)
    # # print(emulator.get_current_state())
    # # print(emulator.get_current_state()["path_covered"])
    # for position in listOfNodes[1:]:
    #     emulator.step(position)
    #     print(emulator.get_current_state())

    result = dynamic_function(1.57,1.57,1.57,1.57)
    print(result)