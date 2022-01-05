import numpy as np
from agent import Agent
from game_env.shapes import *


class AgentH(Agent):
    def __init__(self):
        # [ sum_heights, complete_lines, holes, bumpiness]
        self.weights = [-0.51, 0.76, -0.356, -0.185]
        self.actions = None

    def get_action(self, map, shape, next_shape):
        return np.random.randint(0, 5)
        #if self.actions is None:
        #    pass
            # for rotate (0, max)
                # while can_move left
                    # get move copy
                    # land(map, shape)
                    # calculate heuristic
                    # if max save
                # while can_move right
                    # get move copy
                    # land(map, shape)
                    # calculate heuristic
                    # if max save
            # fill actions with #rotate and #moves
        #return self.actions.pop(0)

    def land(self, map, shape):
        # while can_move down
            # move
        # place
        # return
        pass
