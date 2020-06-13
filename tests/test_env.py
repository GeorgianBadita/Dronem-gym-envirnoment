"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   29.03.2020 20:58
"""
import numpy as np

from env_interpretation.state_utils import get_state_from_observation
from env_interpretation.utils import n_from_prod


def test_env_3(env3_robots):
    env_data = env3_robots.get_env_metadata()
    env3_robots.reset()
    state = env3_robots.get_current_state()
    action = [0, 0, 0]
    action = n_from_prod(env_data['sets'], action)
    new_state, reward, done, _ = env3_robots.step(action)
    new_state_from_obs = get_state_from_observation(new_state)
    assert done == False
    assert reward == -0.666666
    assert state.robots_data == new_state_from_obs.robots_data
    assert state.time + 1 == new_state_from_obs.time
    assert new_state_from_obs.positions == [2, 2, 3]
    assert env3_robots.state.all() == np.array(new_state).all()
    for i in range(3):
        action = [0, 0, 0]
        action = n_from_prod(env_data['sets'], action)
        new_state, reward, done, _ = env3_robots.step(action)
    action = [0, 0, 70]
    action = n_from_prod(env_data['sets'], action)
    new_state, reward, done, _ = env3_robots.step(action)
    assert done == False
    assert reward == 0.001
    assert get_state_from_observation(new_state).time == 6
    assert get_state_from_observation(new_state).robots_data == [15, 30, 0]


def test_env_termination(env4_robots):
    env_data = env4_robots.get_env_metadata()
    env4_robots.reset()
    action_map_terminate = {
        '-1': [0] * 6,
        '2': [25] + [0] * 5,
        '4': [0, 25] + [0] * 4,
        '6': [0] * 5 + [25],
        '8': [0, 25] + [0] * 4
    }
    for i in range(1, 9):
        if action_map_terminate.get(str(i), None):
            action = action_map_terminate[str(i)]
            action = n_from_prod(env_data['sets'], action)
            _, __, done, ___ = env4_robots.step(action)
        else:
            action = action_map_terminate['-1']
            action = n_from_prod(env_data['sets'], action)
            _, __, done, ___ = env4_robots.step(action)
    assert done == True
