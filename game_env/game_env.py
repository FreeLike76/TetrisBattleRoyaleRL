import numpy as np
from game_env.shapes import Shape


class GameEnv:
    def __init__(self):
        # coord
        self.top_hidden = 4
        self.border = 3
        self.map = np.ones((self.top_hidden + 20 + self.border,
                            self.border + 10 + self.border), dtype=np.int32)
        self.map[0: -self.border, self.border: -self.border] = 0

        # shape
        self.shape = None

        # game_env
        self.running = True
        self.score = 0

    def step(self, action):
        # actions:
        # 0 is skip
        # 1 is left
        # 2 is right
        # 3 is down
        # 4 is rotate

        # create new falling object
        if self.shape is None:
            self.shape = Shape()

        # process action
        if action == 1:
            pass
        elif action == 2:
            pass
        elif action == 3:
            pass
        elif action == 4:
            pass
        # check win

        # check lose

        # end

    def can_move(self, x0, y0, figure):
        temp = self.map.copy()
        temp[y0: y0 + figure.shape[0], x0: x0 + figure.shape[1]] += figure
        if 2 in temp:
            return False
        else:
            return True

    def check_row(self):
        temp = self.map.copy()

    def check_lost(self):
        pass
