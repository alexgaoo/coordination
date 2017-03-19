import numpy as np

#################################################################
# Implements a Cooperating Agent Layer for 2D problems

#################################################################

class AgentLayer():

    # constructor
    def __init__(self,
                 xs, # x size of map
                 ys, # y size of map
                 drones): # should we have a seeds array for each agent?
        """
        Each agent must support:
        - move(action)
        - current_position()
        - nactions()
        - set_position(x, y)
        """

        self.drones = drones
        self.nagents = len(drones)
        self.global_state = np.zeros((xs, ys), dtype=np.int32)

    def n_agents(self):
        return self.nagents

    def move_agent(self, agent_idx, action):
        return self.drones[agent_idx].step(action)

    def set_position(self, agent_idx, x, y):
        self.drones[agent_idx].set_position(x,y)

    def get_position(self, agent_idx):
        """
        Returns the position of the given agent
        """
        return self.drones[agent_idx].current_position()

    def get_nactions(self, agent_idx):
        return self.drones[agent_idx].nactions()

    def remove_agent(self, agent_idx):
        # idx is between zero and nagents
        self.drones.pop(agent_idx)
        self.nagents -= 1

    def get_state_matrix(self):
        """
        Returns a matrix representing the positions of all drones
        Example: matrix contains the number of drones at give (x,y) position
        0 0 0 1 0 0 0
        0 2 0 2 0 0 0
        0 0 0 0 0 0 1
        1 0 0 0 0 0 5
        """
        gs = self.global_state
        gs.fill(0)
        for ally in self.drones:
            x, y = ally.current_position()
            gs[x,y] += 1
        return gs

    def get_state(self):
        pos = np.zeros(2*len(self.drones))
        idx = 0
        for ally in self.drones:
            pos[idx:(idx+2)] = ally.get_state()
            idx += 2
        return pos
