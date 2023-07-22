from emulation import Emulation

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

    def run_emulation(self) -> int:
        """
        Perform a single emulation.

        Returns:
            int: The result of the emulation (in this example, a random number).
        """
        emulation = Emulation()
        return emulation.run()

    def run_procedure(self) -> int:
        """
        Run the SimLearnHeuristic procedure.

        Returns:
            int: The best solution found from the emulations.
        """
        while has_enough_budget(self.total_budget, self.timestep_cost):
            result = self.run_emulation()
            self.solution_pool.append(result)
            self.total_budget -= self.timestep_cost

        best_solution = max(self.solution_pool)
        return best_solution

if __name__ == "__main__":
    # Example usage with a budget of 10000 timesteps and an emulation cost of 100 timesteps
    budget: int = 10000
    emulation_cost: int = 100
    number_of_emulations: int = 50

    procedure = SimLearnHeuristic(budget, emulation_cost, number_of_emulations)
    best_solution: int = procedure.run_procedure()

    print("Best Solution:", best_solution)
