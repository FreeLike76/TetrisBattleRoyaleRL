import numpy as np
from agent import Agent
import copy
from game_env.shapes import *
from settings import *


class AgentH(Agent):
    def __init__(self, weights=None):
        # 0 is sum of heights
        # 1 is complete lines
        # 3 is # of holes
        # 4 is bumpiness
        if weights is None:
            self.weights = [-0.6, 0.75, -0.35, -0.2]
        else:
            self.weights = weights

    def get_action(self, game_map, shape, next_shape):
        # NO CHEATING
        if shape.y < GAME_SHAPE_TOP_HIDDEN:
            return 0
        best_action = 0
        best_score = self.heuristic(self.land(game_map.copy(), copy.copy(shape)))

        # IF CAN MOVE LEFT ONCE
        if self.can_move(game_map, shape.x - 1, int(shape.y), shape.get_shape()):
            new_shape = copy.copy(shape)
            new_shape.x -= 1
            score = self.heuristic(self.land(game_map.copy(), new_shape))
            if score > best_score:
                best_score = score
                best_action = 1
            # IF CAN MOVE LEFT TWICE
            if self.can_move(game_map, new_shape.x - 1, int(new_shape.y), new_shape.get_shape()):
                new_shape = copy.copy(new_shape)
                new_shape.x -= 1
                score = self.heuristic(self.land(game_map.copy(), new_shape))
                if score > best_score:
                    best_score = score
                    best_action = 1

        # IF CAN MOVE RIGHT ONCE
        if self.can_move(game_map, shape.x + 1, int(shape.y), shape.get_shape()):
            new_shape = copy.copy(shape)
            new_shape.x += 1
            score = self.heuristic(self.land(game_map.copy(), new_shape))
            if score > best_score:
                best_score = score
                best_action = 2
            # IF CAN MOVE RIGHT TWICE
            if self.can_move(game_map, new_shape.x + 1, int(new_shape.y), new_shape.get_shape()):
                new_shape = copy.copy(new_shape)
                new_shape.x += 1
                score = self.heuristic(self.land(game_map.copy(), new_shape))
                if score > best_score:
                    best_score = score
                    best_action = 2

        # IF CAN ROTATE
        if self.can_move(game_map, shape.x, int(shape.y), shape.get_rotated()):
            new_shape = copy.copy(shape)
            new_shape.rotate()
            score = self.heuristic(self.land(game_map.copy(), new_shape))
            if score > best_score:
                best_score = score
                best_action = 4

        return best_action

    def land(self, temp_map, shape):
        while self.can_move(temp_map, shape.x, int(shape.y + 1), shape.get_shape()):
            shape.y += 1
        x = shape.x
        y = int(shape.y)
        figure = shape.get_shape()
        temp_map[y: y + figure.shape[0], x: x + figure.shape[1]] += figure
        return temp_map

    def can_move(self, temp_map, x0, y0, figure):
        temp = temp_map.copy()
        temp[y0: y0 + figure.shape[0], x0: x0 + figure.shape[1]] += figure
        if 2 in temp:
            return False
        else:
            return True

    def heuristic(self, temp_map):
        # sum of heights
        heights = 24 - np.argmax(temp_map[:, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS] == 1, axis=0)
        sum_hights = heights.sum()

        # bumpiness
        bumpiness = 0
        for i in range(heights.shape[0] - 1):
            bumpiness += abs(heights[i] - heights[i + 1])

        # complete rows
        temp_map = temp_map[GAME_SHAPE_TOP_HIDDEN: -GAME_SHAPE_BORDERS, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS]
        complete_rows = (np.where(temp_map.sum(axis=1) == 10)[0]).size

        # count of holes
        holes = 0
        for i in range(1, temp_map.shape[0]):
            for j in range(temp_map.shape[1]):
                if temp_map[i, j] == 0 and temp_map[i-1, j] == 1:
                    holes += 1

        total = self.weights[0] * sum_hights \
                + self.weights[1] * complete_rows \
                + self.weights[2] * holes \
                + self.weights[3] * bumpiness
        return total
