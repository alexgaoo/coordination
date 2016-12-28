import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)


register(
    id='ButtonOne-v0',
    entry_point='gym_buttons.envs:ButtonOneEnv',
    timestep_limit=1000,
)

register(
    id='ButtonTwo-v0',
    entry_point='gym_buttons.envs:ButtonTwoEnv',
    timestep_limit=1000,
)
