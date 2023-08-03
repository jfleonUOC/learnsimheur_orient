import gymnasium as gym
from gymnasium import spaces
import numpy as np

from emulation import Emulation


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
        self._action_to_direction = {
            0: "pj_heuristic",
            1: "greedy",
        }

        self.emulation = Emulation(nodes, max_cost)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def _get_obs(self):
        obs_dict = {
            "nodes": ,
            "current_pos": ,
            "path_covered": ,
            "x_1": ,
            "x_2": ,
            "x_3": ,
            "x_4": ,
        }
        return {"agent": self._agent_location, "target": self._target_location}

    def _get_info(self):
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Choose the agent's location uniformly at random
        self._agent_location = self.np_random.integers(0, self.size, size=2, dtype=int)

        # We will sample the target's location randomly until it does not coincide with the agent's location
        self._target_location = self._agent_location
        while np.array_equal(self._target_location, self._agent_location):
            self._target_location = self.np_random.integers(
                0, self.size, size=2, dtype=int
            )

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        direction = self._action_to_direction[action]
        # We use `np.clip` to make sure we don't leave the grid
        self._agent_location = np.clip(
            self._agent_location + direction, 0, self.size - 1
        )
        # An episode is done iff the agent has reached the target
        terminated = np.array_equal(self._agent_location, self._target_location)
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