import operator
import numpy as np

# from node import euclidean_distance
from arc import Arc
from importer import Importer

class EfficiencyList():
    """
    The efficiency list is a list containing all* arcs in the node network
    The efficiency list is ordered by efficiency
    The efficiency is calculated as proposed in Panadero et al.(2020) 
    """
    def __init__(self, nodes) -> None:
        self.nodes = nodes
        self.efficiency_list = []

    def __len__(self):
        return len(self.efficiency_list)

    def pop_arc(self, index):
        return self.efficiency_list.pop(index)

    def generate(self, alpha: float):
        """
        the loop starts from node i = 1 (excluding the start) and j = 2
        it does not consider the case when i = j because starts always at i+1
        it also excludes the end node
        """
        for i in range(1, len(self.nodes) - 2):
            for j in range(i + 1, len(self.nodes) - 1):
                node_i = self.nodes[i]
                node_j = self.nodes[j]
                edgeReward = node_i.reward + node_j.reward

                # calculate arc (i,j)
                arc_i_j = Arc(node_i, node_j)
                start_j_arc = Arc(self.nodes[0], node_j)
                i_end_arc = Arc(node_i, self.nodes[-1])
                savings_i_j = start_j_arc.cost + i_end_arc.cost - arc_i_j.cost
                arc_i_j.savings = savings_i_j
                arc_i_j.efficiency = alpha * savings_i_j + (1 - alpha) * edgeReward
                self.efficiency_list.append(arc_i_j)

                # calculate arc (j,i)
                arc_j_i = Arc(node_j, node_i)
                start_i_arc = Arc(self.nodes[0], node_i)
                j_end_arc = Arc(node_j, self.nodes[-1])
                savings_j_i = start_i_arc.cost + j_end_arc.cost - arc_j_i.cost
                arc_j_i.savings = savings_j_i
                arc_j_i.efficiency = alpha * savings_j_i + (1 - alpha) * edgeReward
                self.efficiency_list.append(arc_j_i)

        # sort the list of edges from higher to lower efficiency
        self.efficiency_list.sort(key = operator.attrgetter("efficiency"), reverse = True)
        return self.efficiency_list

    def remove_inverse(self, arc, verbose:bool=False):
        if self.efficiency_list == []:
            print("Empty efficiency list.")    
            return
        for searched_arc in self.efficiency_list:
            if searched_arc.end == arc.start and searched_arc.start == arc.end:
                self.efficiency_list.remove(searched_arc)
                if verbose:
                    print(f"{searched_arc} removed from efficiency list.")
        return

    def filter_node(self, node):
        for arc in self.efficiency_list:
            if arc.start == node or arc.end == node:
                self.efficiency_list.remove(arc)
        return


    def tune_alpha(self):
        #TODO: extract as a function (outside the EfficiencyList class)
        """
        tune the alpha value for generating enhanced savings
        """
        best_reward = 0
        eff_list = []
        alpha = 0
        for new_alpha in np.linspace(0, 1, 11):
            new_effList = EfficiencyList(self.nodes).generate(alpha=new_alpha)
            # new_effList = generateEfficiencyList(nodes, new_alpha)
            # obtain a greedy solution (BR = False) for the current alpha value
            # sol = merging(False, test, fleetSize, routeMaxCost, nodes, new_effList)
            # if sol.reward > best_reward:
                # best_reward = sol.reward
                # eff_list = new_effList
                # init_sol = sol 
            return alpha


if __name__ == "__main__":
    # Import files
    # file_path = "input/ref/set_64_1/set_64_1_15.txt"
    file_path = "input/ref/Tsiligirides 3/tsiligirides_problem_3_budget_070.txt"
    importer = Importer(file_path)
    # importer.print_nodes()
    nodes = importer.node_data

    # Generate efficiency list
    # eff_list = EfficiencyList(nodes,alpha=0.5).generate()
    # for arc in eff_list:
    #     print(f"{arc}: {arc.efficiency}")

    eff_list_05 = EfficiencyList(nodes).generate(alpha=0.5)
    eff_list_02 = EfficiencyList(nodes).generate(alpha=0.2)
    max_05 = max(eff_list_05, key=operator.attrgetter("efficiency"))
    max_02 = max(eff_list_02, key=operator.attrgetter("efficiency"))
    print(max_05.efficiency)
    print(max_02.efficiency)