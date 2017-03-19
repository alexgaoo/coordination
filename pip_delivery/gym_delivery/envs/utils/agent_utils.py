import numpy as np

from six.moves import xrange

from .agent import Agent

def create_agents(nagents, constraints=None):
    """
    Initializes the agents on a map (map_matrix)
    -nagents: the number of agents to put on the map
    -randinit: if True will place agents in random, feasible locations
               if False will place all agents at 0
    """
    agents = []
    for i in xrange(nagents):
        xinit, yinit = (0, 0)
        agent = Agent()
        agent.set_position(xinit, yinit)
        agents.append(agent)
    return agents



