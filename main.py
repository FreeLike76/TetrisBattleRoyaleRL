import tensorflow as tf
from game import *
from agent_rl.agent_rl import AgentRL
from agent_h.agent_h import AgentH
from agent_rand.agent_rand import AgentRand


if __name__ == "__main__":
    physical_devices = tf.config.list_physical_devices("GPU")
    try:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
    except:
        pass

    agents = {#"Rand": AgentRand(),
              "Agent-RL9": AgentRL(r"agent_rl/saved/dqn_v9.h5", skip_action=False),
              "Agent-RL14": AgentRL(r"agent_rl/saved/dqn_v14.h5", skip_action=True),
              "Agent-RL18": AgentRL(r"agent_rl/saved/dqn_v18.h5", skip_action=True),
              "Agent-RL20": AgentRL(r"agent_rl/saved/dqn_v20.h5", skip_action=True)
              #"Heuristic": AgentH()
              }

    app = Game(agents)
    app.run()
