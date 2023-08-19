import gymnasium as gym
from gymnasium import spaces
import numpy as np

from emulation import Emulation, dynamic_param
from heuristic import pj_heuristic, generate_new_route, find_max_reward_node


class OrienteeringEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"]}

    def __init__(self, nodes, max_cost, render_mode=None):

        # Observations are dictionaries with the list of nodes, current position, path covered and conditions.
        # There is the possibility of defining a Graph space (TODO)
        self.observation_space = spaces.Dict(
            {
                # "nodes": spaces.Sequence(spaces.Box(0, 100, dtype=int)),
                "nodes": spaces.Sequence(spaces.Discrete(len(nodes))),
                # "current_pos": spaces.Box(0, 100, dtype=int),
                "current_pos": spaces.Discrete(len(nodes)),
                # "path_covered": spaces.Sequence(spaces.Box(0, 100, dtype=int)),
                "path_covered": spaces.Sequence(spaces.Discrete(len(nodes))),
                # "conditions": spaces.Tuple(spaces.Box(0, 1, dtype=float32)),
                "x_1": spaces.Box(0, 1, dtype=float),
                "x_2": spaces.Box(0, 1, dtype=float),
                "x_3": spaces.Box(0, 1, dtype=float),
                "x_4": spaces.Box(0, 1, dtype=float),
            }
        )

        # We have 2 actions: "pj_heuristic", "greedy"
        self.action_space = spaces.Discrete(2)
        # dict to map abstract actions to real actions
        self._action_to_heuristic = {
            0: "pj_heuristic",
            1: "greedy",
        }

        self.emulation = Emulation(nodes, max_cost)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def _get_obs(self):
        """
        Funtion to return a dictionary with the environment observations
        - nodes: the available nodes (all minus the covered path)
        - current position (only id - integer)
        - path covered
        - dynamic conditions (x1, x2...)
        """
        obs_dict = {
            "nodes": [x.id for x in self.emulation.nodes if x not in self.emulation.path_covered],
            "current_pos": self.emulation.current_node.id,
            "path_covered": [x.id for x in self.emulation.path_covered],
            "x_1": self.emulation.parameters[0],
            "x_2": self.emulation.parameters[1],
            "x_3": self.emulation.parameters[2],
            "x_4": self.emulation.parameters[3],
        }
        return obs_dict

    def _get_info(self):
        return {
            "step_number": len(self.emulation.path_covered)
        }

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.emulation.reset_emulator()

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        # Map the action (element of {0,1}) to the type of heuristic 
        heuristic = self._action_to_heuristic[action]
        if heuristic == "pj_heuristic":
            # run the pj heuristic and select the best option
            self.emulation.update_parameters(dynamic_param())
            solution = generate_new_route(self.emulation)
            next_node = solution.get_best_route().get_nodes()[1]
        elif heuristic == "greedy":
            # find the next node with the maximum (local) reward
            next_node = find_max_reward_node(self.emulation)
        self.emulation.step(next_node.id)

        # An episode is done (terminated) if the vehicles arrives to the final node
        # No truncated situation (always valued as False)
        # if 
        terminated = np.array_equal(self._agent_location, self._target_location)
        
        #TODO: Reward every step based on the partial increase in score?
        #TODO: Reward at the end based on the total score achieved?
        reward = 1 if terminated else 0  # Binary sparse rewards

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info 

    """
    Rendering
    """
    #TODO:
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()