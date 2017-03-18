import numpy as np

from six.moves import xrange

from .agent import Agent

def create_agents(nagents, map_matrix, obs_range, constraints=None):
    """
    Initializes the agents on a map (map_matrix)
    -nagents: the number of agents to put on the map
    -randinit: if True will place agents in random, feasible locations
               if False will place all agents at 0
    """
    xs, ys = map_matrix.shape
    agents = []
    for i in xrange(nagents):
        xinit, yinit = (0, 0)
        agent = Agent(xs, ys, map_matrix, obs_range=obs_range)
        agent.set_position(xinit, yinit)
        agents.append(agent)
    return agents



def set_agents(agent_matrix, map_matrix):
    # check input sizes
    if agent_matrix.shape != map_matrix.shape:
        raise ValueError("Agent configuration and map matrix have mis-matched sizes")

    agents = []
    xs, ys = agent_matrix.shape
    for i in xrange(xs):
        for j in xrange(ys):
            n_agents = agent_matrix[i, j]
            if n_agents > 0:
                if map_matrix[i, j] == -1:
                    raise ValueError(
                        "Trying to place an agent into a building: check map matrix and agent configuration")
                agent = Agent(xs, ys, map_matrix)
                agent.set_position(i, j)
                agents.append(agent)
    return agents
