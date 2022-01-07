import numpy as np

from agent import Agent
from settings import *

import tensorflow as tf
import tensorflow.keras.layers as layers

from rl.agents import DQNAgent
from rl.policy import MaxBoltzmannQPolicy
from rl.memory import SequentialMemory


class AgentRL(Agent):
    def __init__(self, path, skip_action=False):
        self.skip_action = int(skip_action)
        self.model = tf.keras.Sequential([
            # 1 state, 20 rows, 10 cols, 3 matricies: locked, falling and next figures
            layers.Input(shape=(1, 20, 10, 3)),
            layers.Reshape(target_shape=(20, 10, 3)),

            layers.Conv2D(filters=32, kernel_size=(3, 3), padding="same"),
            layers.Activation("relu"),
            layers.MaxPool2D(),

            layers.Conv2D(filters=64, kernel_size=(3, 3), padding="same"),
            layers.Activation("relu"),
            layers.MaxPool2D(),

            layers.Flatten(),

            layers.Dense(32),
            layers.Activation("relu"),

            layers.Dense(16),
            layers.Activation("relu"),

            layers.Dense(4 + int(self.skip_action))])

        policy = MaxBoltzmannQPolicy(eps=0.2)
        memory = SequentialMemory(limit=2048, window_length=1)
        self.dqn = DQNAgent(model=self.model,
                            memory=memory,
                            policy=policy,
                            nb_actions=4+int(self.skip_action),
                            gamma=0.99,
                            nb_steps_warmup=256,
                            batch_size=64,
                            target_model_update=0.01,
                            enable_double_dqn=True,
                            enable_dueling_network=True)

        self.dqn.compile(tf.keras.optimizers.Adam(learning_rate=0.001, clipnorm=1.0), metrics=["mean_squared_error"])
        self.dqn.load_weights(path)

    def _encode_observation(self, game_map, shape, next_shape):
        # observable map
        temp_map = game_map[GAME_SHAPE_TOP_HIDDEN:-GAME_SHAPE_BORDERS, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS].copy()

        # observation of cur shape on map
        temp_shape = np.zeros(game_map.shape)
        x0 = shape.x
        y0 = int(shape.y)
        this_shape = shape.get_shape()
        temp_shape[y0: y0 + this_shape.shape[0], x0: x0 + this_shape.shape[1]] += this_shape
        temp_shape = temp_shape[GAME_SHAPE_TOP_HIDDEN:-GAME_SHAPE_BORDERS, GAME_SHAPE_BORDERS: -GAME_SHAPE_BORDERS]

        # next shape on map, assuming y0 = 0
        temp_next_shape = np.zeros((20, 10))
        x0 = next_shape.x - GAME_SHAPE_BORDERS
        next_shape = next_shape.get_shape()
        temp_next_shape[0: next_shape.shape[0], x0: x0 + next_shape.shape[1]] += next_shape

        return np.stack([temp_map, temp_shape, temp_next_shape], axis=-1).astype(np.float32)

    def get_action(self, game_map, shape, next_shape):
        observation = self._encode_observation(game_map, shape, next_shape)
        action = self.dqn.forward(observation)
        if self.skip_action:
            return action
        else:
            return action + 1
