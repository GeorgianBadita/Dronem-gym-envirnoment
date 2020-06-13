"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   21.03.2020 23:47
"""

from env_interpretation.state_utils import get_state_from_observation, get_observation_from_state


def test_get_state_from_observation(env3_robots):
    sample = env3_robots.observation_space.sample()
    sample = list(sample)
    state_from_obs = get_state_from_observation(sample)
    assert sample[:3] == state_from_obs.robots_data
    assert sample[3] == state_from_obs.time
    assert sample[4:] == state_from_obs.positions
    assert get_observation_from_state(state_from_obs) == sample
