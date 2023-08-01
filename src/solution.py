import operator
import copy

from node import Node, euclidean_distance
from arc import Arc
from route import Route
from importer import Importer

class Solution():
    def __init__(self, id: int = 0) -> None:
        self.id = id
        self.candidate_routes = []

    def get_best_route(self):
        best_route = None
        if not self.candidate_routes:
            print("No routes available in solution.")
            return None
        # sort the list of routes in sol by reward and cost
        self.candidate_routes.sort(key = operator.attrgetter("cost"), reverse = False)
        self.candidate_routes.sort(key = operator.attrgetter("reward"), reverse = True)
        best_route = self.candidate_routes[0]
        return best_route

    def add_route(self, route: Route):
        self.candidate_routes.append(route)

    def remove_route(self, route: Route):
        self.candidate_routes.remove(route)

    def get_route_by_node(self, node):
        for route in self.candidate_routes:
            # print(route)
            for arc in route.arcs:
                if arc.start == node or arc.end == node:
                    return route
        # print(f"Node {node.id} not found in route.")
        return None


def dummy_solution(input_nodes, route_max_cost):
    """
    If any dummy route has a higher cost than the max cost allowed it is not consider in the solution
    """
    solution = Solution()
    available_nodes = copy.copy(input_nodes)
    start_node = find_start_node(available_nodes) 
    end_node = find_end_node(available_nodes)
    available_nodes.remove(start_node)
    available_nodes.remove(end_node)
    for node in available_nodes: # excludes the start_node and end_node 
        start_arc = Arc(start_node, node) # creates the (start_node, node) edge (arc)
        end_arc = Arc(node, end_node) # creates the (node, end_node) edge (arc)
        route = Route()
        route.add_arc(start_arc)
        route.add_arc(end_arc)
        if route.cost <= route_max_cost:
            solution.add_route(route)
    print(f"Dummy solution created with {len(solution.candidate_routes)} routes")
    return solution

def find_start_node(node_list):
    """
    Given a network (list of nodes), find the starting node (depot)
    """
    for node in node_list:
        if node.is_start:
            return node
    print("No starting node found.")
    return None

def find_end_node(node_list):
    """
    Given a network (list of nodes), find the starting node (depot)
    """
    for node in node_list:
        if node.is_end:
            return node
    print("No starting node found.")
    return None


if __name__ == "__main__":
    # Import files
    # file_path = "input/ref/set_64_1/set_64_1_15.txt"
    # file_path = "input/ref/Tsiligirides 3/tsiligirides_problem_3_budget_070.txt"
    file_path = "input/ref/Tsiligirides 1/tsiligirides_problem_1_budget_05 - Copy.txt"
    importer = Importer(file_path)
    # importer.print_nodes()
    nodes = importer.node_data
    routeMaxCost = importer.Tmax

    # Create dummy solution
    dummy_sol = dummy_solution(nodes, routeMaxCost)
    for route in dummy_sol.candidate_routes:
        print(route)
    
    # dummy_sol.remove_route(dummy_sol.candidate_routes[0])
    # for route in dummy_sol.candidate_routes:
        # print(route)
