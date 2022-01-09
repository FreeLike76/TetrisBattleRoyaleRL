import numpy as np
from game_env.shapes import Shape
from settings import *
from gym import Env
from gym.spaces import Discrete


class GameEnv(Env):
    def __init__(self):
        self.action_space = Discrete(5)
        self.observation_space = None
        # coord
        self.map = np.ones((GAME_SHAPE_TOP_HIDDEN + 20 + GAME_SHAPE_BORDERS,
                            GAME_SHAPE_BORDERS + 10 + GAME_SHAPE_BORDERS), dtype=np.int32)
        self.map[0: -GAME_SHAPE_BORDERS, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS] = 0

        # params
        self.gravity = FALL_SPEED

        # shape
        self.shape = Shape()
        self.next_shape = Shape()

        # game_env
        self.running = True

    def step(self, action):
        reward = 0
        if not self.running:
            return self._state_observe(), reward, not self.running, {}
        reward += self._reward_for_alive()
        # actions:
        # 0 is skip
        if action == 0:
            reward += self._reward_for_skip_action()
        # 1 is left
        if action == 1:
            if self.can_move(self.shape.x - 1, int(self.shape.y), self.shape.get_shape()):
                self.shape.x -= 1
        # 2 is right
        elif action == 2:
            if self.can_move(self.shape.x + 1, int(self.shape.y), self.shape.get_shape()):
                self.shape.x += 1
        # 3 is down
        elif action == 3:
            if self.can_move(self.shape.x, int(self.shape.y + 1), self.shape.get_shape()):
                self.shape.y += 1
        # 4 is rotate
        elif action == 4:
            if self.can_move(self.shape.x, int(self.shape.y), self.shape.get_rotated()):
                self.shape.rotate()

        # move down
        if self.can_move(self.shape.x, int(self.shape.y + self.gravity), self.shape.get_shape()):
            self.shape.y += self.gravity
        else:
            self.lock_figure()
            reward += self._reward_after_lock_figure()

        cleared = self.remove_full_rows()
        reward += self._reward_for_clear_rows(cleared)

        return self._state_observe(), reward, not self.running, {}

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
        y = int(self.shape.y)
        figure = self.shape.get_shape()
        self.map[y: y + figure.shape[0], x: x + figure.shape[1]] += figure
        self.shape = self.next_shape
        self.next_shape = Shape()
        if y < GAME_SHAPE_TOP_HIDDEN:
            self.running = False

    def remove_full_rows(self):
        cleared = 0
        full = self.map[GAME_SHAPE_TOP_HIDDEN: -GAME_SHAPE_BORDERS, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS]
        full = np.where(full.sum(axis=1) == 10)[0]
        if full.size > 0:
            cleared = full.size

            # to get indexes of the game screen
            full = full + GAME_SHAPE_TOP_HIDDEN

            # remove full rows
            self.map[full, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS] = 0

            # get non-empty rows
            partial = self.map[GAME_SHAPE_TOP_HIDDEN: -GAME_SHAPE_BORDERS, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS]
            partial = np.where(partial.sum(axis=1) != 0)[0]

            # if there are levitating non-empty rows
            if partial.size > 0:
                # get their indexes
                partial = partial + GAME_SHAPE_TOP_HIDDEN
                bottom = self.map.shape[0] - GAME_SHAPE_BORDERS
                # move them to bottom
                self.map[bottom-partial.size: bottom, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS] = \
                    self.map[partial, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS]
                # everything above must be cleared
                self.map[0: bottom-partial.size, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS] = 0
        return cleared

    def _reward_for_alive(self):
        return 0

    def _reward_for_skip_action(self):
        return 0

    def _reward_after_lock_figure(self):
        return 1

    def _reward_for_clear_rows(self, cleared):
        return cleared * 10

    def _state_gen(self):
        """Re-init state of game"""
        self.running = True

        self.map = np.ones((GAME_SHAPE_TOP_HIDDEN + 20 + GAME_SHAPE_BORDERS,
                            GAME_SHAPE_BORDERS + 10 + GAME_SHAPE_BORDERS), dtype=np.int32)
        self.map[0: -GAME_SHAPE_BORDERS, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS] = 0

        self.shape = Shape()
        self.next_shape = Shape()

    def render(self, mode="human"):
        """What to visualize"""
        pass

    def reset(self):
        """Reset the state to start"""
        # restart state
        self._state_gen()
        # not terminal
        return self._state_observe()

    def _state_observe(self):
        """
        What the agent will see during training
        Later this function will have to be implemented in agent's class
        The inputs will be: map, shape, next_shape
        """
        return None
