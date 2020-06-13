"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   20.03.2020 00:48
"""

import pytest

from dronem_gym_env.envs import DronemEnv
from env_interpretation import Exchange


@pytest.fixture()
def dronem_env():
    return DronemEnv(
        num_robots=3,
        max_memory=3,
        init_memory=1
    )


def test_get_action_from_num(dronem_env):
    """
    Function to test the get action number function
    """
    metadata = dronem_env.get_env_metadata()
    max_memory = metadata['max_memory']

    pair_mapping = [(0, 1), (0, 2), (1, 2)]
    interpreted_actions = [
        (Exchange(pair_mapping[0][0], pair_mapping[0][1], i),
         Exchange(pair_mapping[1][0], pair_mapping[1][1], j),
         Exchange(pair_mapping[2][0], pair_mapping[2][1], k))
        for i in range(-3, 4)
        for j in range(-3, 4)
        for k in range(-3, 4)
    ]
    assert len(interpreted_actions) == len(set(interpreted_actions))
    assert dronem_env.lazy_action_get.max_size == (2 * max_memory + 1) ** metadata['num_robots']
    all_actions_from_function = [
        tuple(dronem_env.get_action_from_space(i))
        for i in range((2 * max_memory + 1) ** metadata['num_robots'])
    ]

    assert len(all_actions_from_function) == len(set(all_actions_from_function))
    assert dronem_env.get_action_from_space(0) == [Exchange(0, 1, 0), Exchange(0, 2, 0),
                                                   Exchange(1, 2, 0)]
    for exchange in interpreted_actions:
        assert exchange in all_actions_from_function
