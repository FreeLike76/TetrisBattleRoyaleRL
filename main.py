from game import *
from agent_rl.agent_rl import AgentRL
from agent_h.agent_h import AgentH
from agent_rand.agent_rand import AgentRand

if __name__ == "__main__":
    # "Agent-RL": AgentRL(r"agent_rl/saved/dqn_v9.h5"),
    agents = {"Rand": AgentRand(),
              "Rand2": AgentRand(),
              "Heuristic": AgentH()}

    app = Game(agents)
    app.run()