import tensorflow as tf


class Agent:
    def __init__(self):
        self.agent = None
        self.model = None

    def build_model(self):
        pass

    def build_agent(self):
        pass

    def load_model_weights(self):
        pass

    def encode_observation(self, observation):
        pass

    def get_action(self, observation):
        pass
