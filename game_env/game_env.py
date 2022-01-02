import numpy as np
from shapes import Shape


class GameEnv:
    def __init__(self):
        # coord
        self.top_hidden = 4
        self.border = 3
        self.map = np.ones((self.top_hidden + 20 + self.border,
                            self.border + 10 + self.border), dtype=np.int32)
        self.map[0: -3, 3: -3] = 0

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

    def can_move(self):
        pass

    def check_row(self):
        pass

    def check_lost(self):
        pass
