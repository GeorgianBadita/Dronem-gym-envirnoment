"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   11.03.2020 22:53
"""

from gym.envs.registration import register

register(
    id='dronem-v0',
    entry_point='dronem_gym_env.envs:DronemEnv',
)