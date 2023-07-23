import operator

from node import Node, euclidean_distance
from arc import Arc
from route import Route
from importer import Importer

class Solution():
    def __init__(self, id: int = 0) -> None:
        self.id = id
        self.candidate_routes = []
        self.best_route = None

    def get_best_route(self):
        if not self.candidate_routes:
            print("No routes available in solution.")
            return None
        # sort the list of routes in sol by reward and cost
        self.candidate_routes.sort(key = operator.attrgetter("cost"), reverse = False)
        self.candidate_routes.sort(key = operator.attrgetter("reward"), reverse = True)
        # self.best_route = max(self.candidate_routes, key=operator.attrgetter("reward"))
        self.best_route = self.candidate_routes[0]
        return self.best_route

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
        print(f"Node {node.id} not found in route.")
        return None


def dummy_solution(nodes, route_max_cost):
    """
    If any dummy route has a higher cost than the max cost allowed it is not consider in the solution
    """
    solution = Solution()
    start_node = nodes[0]
    end_node = nodes[-1]
    for node in nodes[1:-1]: # excludes the start_node and end_node 
        start_arc = Arc(start_node, node) # creates the (start_node, node) edge (arc)
        end_arc = Arc(node, end_node) # creates the (node, end_node) edge (arc)
        route = Route()
        route.add_arc(start_arc)
        route.add_arc(end_arc)
        if route.cost <= route_max_cost:
            solution.add_route(route)
    print(f"Dummy solution created with {len(solution.candidate_routes)} routes")
    return solution



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
