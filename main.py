from game import *
from agent_rl.agent_rl import AgentRL
from agent_h.agent_h import AgentH
from agent_rand.agent_rand import AgentRand

if __name__ == "__main__":

    agents = {"Rand": AgentRand(),
              "Agent-RL": AgentRL(r"agent_rl/saved/dqn_v9.h5"),
              "Heuristic": AgentH()}
    app = Game(agents)
    app.run()
