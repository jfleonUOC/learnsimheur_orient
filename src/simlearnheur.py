from importer import Importer
from efficiencylist import EfficiencyList
from emulation import Emulation, dynamic_param
from heuristic import pj_heuristic, generate_new_route

def has_enough_budget(budget: int, timestep_cost: int) -> bool:
    """
    Check if there's enough budget to run a single emulation.

    Parameters:
        budget (int): The available budget in timesteps.
        timestep_cost (int): The cost of a single emulation in timesteps.

    Returns:
        bool: True if there's enough budget, False otherwise.
    """
    return budget >= timestep_cost

class SimLearnHeuristic:
    def __init__(self, total_budget: int, timestep_cost: int, num_simulations: int):
        """
        Initialize the SimLearnHeuristic instance.

        Parameters:
            total_budget (int): The total budget in timesteps.
            timestep_cost (int): The cost of a single emulation in timesteps.
            num_simulations (int): The number of emulations to be performed.
        """
        self.total_budget = total_budget
        self.timestep_cost = timestep_cost
        self.num_simulations = num_simulations
        self.solution_pool = []

    def initialize(self, path):
        importer = Importer(path)
        # importer.print_nodes()
        nodes = importer.node_data
        routeMaxCost = importer.Tmax

        return nodes, routeMaxCost

    def run_heuristic(self, type, nodes, max_cost) -> Emulation:
        """
        Run the heuristic procedure of the selected "type":
            - "basic_pj": request new route using PJ heuristic for next emulation step
        """
        if type == "basic_pj":
            emulator = Emulation(nodes, max_cost)
            eff_list = EfficiencyList(nodes)
            eff_list.generate(alpha=0.5)
            #TODO: stoping condition outside emulator required: a new step is still feasible?
            remaining_nodes_num = float("inf")
            while remaining_nodes_num > 1:
                solution = generate_new_route(emulator)
                if solution:
                    emulator.update_parameters(dynamic_param())
                    emulator.step(solution.get_best_route().get_nodes()[1])
                    print(emulator.get_current_state())
                    remaining_nodes_num = len(solution.candidate_routes)
                else:
                    break
            emulator.step(nodes[-1].id) # perform last step to final node (depot)
            return emulator
        else:
            print("Invalid type.")
            return None

    def run_procedure(self) -> int:
        """
        Run the SimLearnHeuristic procedure.

        Returns:
            int: The best solution found from the emulations.
        """
        while has_enough_budget(self.total_budget, self.timestep_cost):
            result = self.run_emulation()
            self.solution_pool.append(result)
            #TODO: use time or resource module to know the timestep_cost of running each solution
            self.total_budget -= self.timestep_cost

        best_solution = max(self.solution_pool)
        return best_solution

if __name__ == "__main__":
    # Example usage with a budget of 10000 timesteps and an emulation cost of 100 timesteps
    budget: int = 10000
    emulation_cost: int = 100
    number_of_emulations: int = 50

    # procedure = SimLearnHeuristic(budget, emulation_cost, number_of_emulations)
    # best_solution: int = procedure.run_procedure()
    # print("Best Solution:", best_solution)

    # file_path = "input/ref/Tsiligirides 1/tsiligirides_problem_1_budget_05 - Copy.txt"
    file_path = "input/ref/Tsiligirides 3/tsiligirides_problem_3_budget_070.txt"
    # file_path = "input/ref/set_64_1/set_64_1_15.txt"
    procedure = SimLearnHeuristic(budget, emulation_cost, number_of_emulations)
    network, maxCost = procedure.initialize(file_path)
    result = procedure.run_heuristic("basic_pj", network, maxCost)
    print(result.get_current_state())
