import math
import random
import copy
import operator

from node import euclidean_distance
from efficiencylist import EfficiencyList
from solution import Solution, dummy_solution
from importer import Importer

def getRandomPosition(size, beta1:float = 0.1, beta2:float = 0.3):
    """
    Gets a random position according to a Gemetric(beta)
    """
    # randomly select a beta value between beta1 and beta2
    # the default values 0.1 and 0.3 were taken from the one used in Panadero et al.(2020)
    beta = beta1 + random.random() * (beta2 - beta1)
    index = int(math.log(random.random())/math.log(1 - beta))
    index = index % size
    return index

def checkMergingConditions(iNode, jNode, iRoute, jRoute, ijArc, routeMaxCost, verbose:bool=True):
    """ Check if merging conditions are met """
    # condition 1: iRoute and jRoure are not the same route object
    if iRoute == jRoute:
        if verbose: print("cannot merge routes: same routes")
        return False
    # condition 2.1: The route with the node(i) has to be linked to end
    if iRoute.is_linked_to_end(iNode) == False:
        if verbose: print(f"cannot merge routes: {iNode}(i) not linked to end")
        return False
    # condition 2.2: The route with the node(j) has to be linked to start
    if jRoute.is_linked_to_start(jNode) == False:
        if verbose: print(f"cannot merge routes: {jNode}(j) not linked to start")
        return False
    # condition 3: cost after merging does not exceed maxTime (or maxCost)
    # print(f"{routeMaxCost =}")
    # print(f"{iRoute=}, cost={iRoute.cost}")
    # print(f"{jRoute=}, cost={jRoute.cost}")
    # print(f"{ijArc=}, savings={ijArc.savings}")
    if iRoute.cost + jRoute.cost - ijArc.savings > routeMaxCost:
        if verbose: print("cannot merge routes: cost exceeded")
        return False
    # else, merging is feasible
    return True

def pj_heuristic(nodes, eff_list, routeMaxCost, useBR:bool=True, verbose:bool=False):
    """ Perform the BR arc-selection & routing-merging iterative process """
    sol = dummy_solution(nodes, routeMaxCost) # compute the dummy solution
    if len(sol.candidate_routes) == 0:
        print("No candidate routes in dummy solution.")
        return None
    elif len(sol.candidate_routes) == 1:
        print("Only one solution - no merge is possible")
        return sol
    effList = copy.copy(eff_list) # make a shallow copy of the effList since it will be modified
    while len(effList) > 0: # list is not empty
        position = 0
        if useBR == True:
            position = getRandomPosition(len(effList))
        else:
            position = 0  # greedy behavior
        arc_i_j = effList.pop_arc(position) # select the next arc from the list
        # determine the nodes i < j that define the arc
        node_i = arc_i_j.start
        node_j = arc_i_j.end
        # determine the routes associated with each node
        route_i = sol.get_route_by_node(node_i)
        if route_i is None:
            effList.filter_node(node_i)
            continue
        route_j = sol.get_route_by_node(node_j)
        if route_j is None:
            effList.filter_node(node_j)
            continue
        if verbose:
            print(f"*** NEW ARC ***")
            print(f"efflist: {len(effList)}")
            print(f"initial routes in sol: {len(sol.candidate_routes)}")
            print(f"{arc_i_j =} -> Reward_start={arc_i_j.start.reward}, Cost={arc_i_j.cost}")
            print(f"{arc_i_j =} -> Reward_end={arc_i_j.end.reward}, Cost={arc_i_j.cost}")
            print(f"{route_i =} -> Reward={route_i.reward}, Cost={route_i.cost}")
            print(f"{route_j =} -> Reward={route_j.reward}, Cost={route_j.cost}")
        # print(f"efflist: {len(effList)}")
        # check if merge is possible
        isMergeFeasible = checkMergingConditions(node_i, node_j, route_i, route_j, arc_i_j, routeMaxCost, verbose)
        # if all necessary conditions are satisfied, merge and delete arc (j, i)
        if isMergeFeasible:
            if verbose:
                print(f"merging")
            # route_i will contain arc (i, finish)
            arc_i = route_i.arcs[-1] # arc_i is (i, finish)
            route_i.remove_arc(arc_i) # node i will not be linked to finish depot anymore
            # route_j will contain arc (start, j)
            arc_j = route_j.arcs[0]
            route_j.remove_arc(arc_j) # node j will not be linked to start depot anymore

            # add arc_i_j to route_i
            route_i.add_arc(arc_i_j)
            # route_i.reward += node_j.reward

            # add route_j to new route_i
            for arc in route_j.arcs:
                route_i.add_arc(arc)
                # route_i.reward += arc.end.reward
            if verbose:
                print(f"{route_i =} -> Reward={route_i.reward}, Cost={route_i.cost}")

            # delete route_j from emerging solution
            sol.remove_route(route_j)

            # if still in list, delete arc (j, i) since it will not be used
            effList.remove_inverse(arc_i_j, verbose)

        if verbose:
            print(f"n routes in sol: {len(sol.candidate_routes)}")
            for route in sol.candidate_routes:
                print(f"* {route}")

    # sort the list of routes in sol by reward and cost
    sol.candidate_routes.sort(key = operator.attrgetter("cost"), reverse = False)
    sol.candidate_routes.sort(key = operator.attrgetter("reward"), reverse = True)
    print("*** Routes after merging ***")
    for route in sol.candidate_routes:
        print(f"* {route} -> Reward={route.reward}, Cost={route.cost}")

    return sol

def generate_new_route(emulation, verbose:bool=False) -> Solution:
    """
    Given the current status (emulation network, current position, route covered)
    generate a new route to the end position based on the the selected heuristic
    (with the PJ's heuristic the new routes are always feasible)
    """
    #TODO: function to clean up the efficiency list
    #   - parameter to clean also the inverse arc
    new_nodes = copy.copy(emulation.nodes) # create a shallow copy of the emulation nodes
    for visited_node in emulation.path_covered[:-1]:
        new_nodes.remove(visited_node) # remove the already visited nodes
    new_eff_list = EfficiencyList(new_nodes)
    new_eff_list.generate(alpha=0.5) # calculate a new efficiency list
    new_max_cost = emulation.get_initial_conditions()["initial_max_cost"] - emulation.static_cost
    # generate a new solution using the PJ's algrorithm
    emulation.path_covered[-1].is_start = True # make final node in path the starting node
    if dummy_solution(new_nodes, new_max_cost):
        new_solution = pj_heuristic(new_nodes, new_eff_list, new_max_cost, useBR=False, verbose=verbose)
    emulation.path_covered[-1].is_start = False # final node in covered path is not the starting node

    return new_solution

def find_max_reward_node(emulation):
    """
    Function to find the node with the max reward for a given emulation (with its current status)
    TODO: change to max efficiency node (balance between reward and distance)
    TODO: add a control to make the route feasible and to end the route if not feasible
    """
    candidate_nodes = list(set(emulation.nodes).difference(emulation.path_covered))
    max_reward = 0
    dist_cost = float("inf")
    for node in candidate_nodes:
        if node.reward > max_reward:
            max_reward = node.reward
            max_reward_node = node
            dist_cost = euclidean_distance(emulation.current_node, node)
        elif node.reward == max_reward:
            new_cost_dist = euclidean_distance(emulation.current_node, node)
            if new_cost_dist < dist_cost:
                max_reward = node.reward
                max_reward_node = node
                dist_cost = new_cost_dist
    return max_reward_node

def find_max_eff_node(emulation):
    """
    Function to find the node with the max efficiency for a given emulation (with its current status)
    TODO: change to max efficiency node (balance between reward and distance)
    TODO: add a control to make the route feasible and to end the route if not feasible
    """
    candidate_nodes = list(set(emulation.nodes).difference(emulation.path_covered))
    max_reward = 0
    dist_cost = float("inf")
    for node in candidate_nodes:
        if node.reward > max_reward:
            max_reward = node.reward
            max_reward_node = node
            dist_cost = euclidean_distance(emulation.current_node, node)
        elif node.reward == max_reward:
            new_cost_dist = euclidean_distance(emulation.current_node, node)
            if new_cost_dist < dist_cost:
                max_reward = node.reward
                max_reward_node = node
                dist_cost = new_cost_dist
    return max_reward_node


if __name__ == "__main__":
    # Import files
    file_path = "input/ref/set_64_1/set_64_1_15.txt"
    # file_path = "input/ref/Tsiligirides 3/tsiligirides_problem_3_budget_070.txt"
    # file_path = "input/ref/Tsiligirides 1/tsiligirides_problem_1_budget_05 - Copy.txt"
    importer = Importer(file_path)
    # importer.print_nodes()
    nodes = importer.node_data
    routeMaxCost = importer.Tmax

    # Generate efficiency list
    eff_list = EfficiencyList(nodes)
    eff_list.generate(alpha=0.5)

    # Run PJ Heuristic
    merged_sol = pj_heuristic(nodes, eff_list, routeMaxCost, useBR=True, verbose=False)
    listOfNodes = merged_sol.get_best_route().get_nodes()
    print(listOfNodes)