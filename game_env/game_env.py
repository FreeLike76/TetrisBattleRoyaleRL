import numpy as np
from game_env.shapes import Shape
from settings import *


class GameEnv:
    def __init__(self):
        # coord
        self.map = np.ones((GAME_SHAPE_TOP_HIDDEN + 20 + GAME_SHAPE_BORDERS,
                            GAME_SHAPE_BORDERS + 10 + GAME_SHAPE_BORDERS), dtype=np.int32)
        self.map[0: -GAME_SHAPE_BORDERS, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS] = 0

        # shape
        self.shape = Shape()
        self.next_shape = Shape()

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
        if action == 1:
            if self.can_move(self.shape.x - 1, int(self.shape.y), self.shape.get_shape()):
                self.shape.x -= 1
        elif action == 2:
            if self.can_move(self.shape.x + 1, int(self.shape.y), self.shape.get_shape()):
                self.shape.x += 1
        elif action == 3:
            if self.can_move(self.shape.x, int(self.shape.y + 1), self.shape.get_shape()):
                self.shape.y += 1
            else:
                self.lock_figure()
        elif action == 4:
            if self.can_move(self.shape.x, int(self.shape.y), self.shape.get_rotated()):
                self.shape.rotate()

        # move down
        if self.can_move(self.shape.x, int(self.shape.y + FALL_SPEED), self.shape.get_shape()):
            self.shape.y += FALL_SPEED
        else:
            self.lock_figure()


        # check win
        # check lose
        # end

    def at(self, x, y):
        return self.map[GAME_SHAPE_TOP_HIDDEN + y, GAME_SHAPE_BORDERS + x]

    def can_move(self, x0, y0, figure):
        temp = self.map.copy()
        temp[int(y0): int(y0 + figure.shape[0]), x0: x0 + figure.shape[1]] += figure
        if 2 in temp:
            return False
        else:
            return True

    def lock_figure(self):
        x = self.shape.x
        y = self.shape.y
        figure = self.shape.get_shape()
        self.map[int(y): int(y + figure.shape[0]), x: x + figure.shape[1]] += figure
        self.shape = self.next_shape
        self.next_shape = Shape()

    def check_row(self):
        temp = self.map.copy()

    def check_lost(self):
        pass
