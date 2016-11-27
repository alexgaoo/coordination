import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

# Gazebo
# ----------------------------------------

# Turtlebot envs
register(
    id='Physics-v0',
    entry_point='gym_physics.envs:GazeboPointSimpleCameraLocation',
    # More arguments here
)
