import numpy as np
from agent import Agent


class AgentRand(Agent):
    def get_action(self, map, shape, next_shape):
        return np.random.randint(0, 5)
