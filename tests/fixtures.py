"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   22.03.2020 00:21
"""
import pytest

from dronem_gym_env.envs import DronemEnv
from env_interpretation import Meeting


@pytest.fixture
def env4_robots():
    """
    Returns the environment, alongside its pair mapping
    :return:
    """
    return DronemEnv(
        num_robots=4,
        max_memory=15,
        init_memory=10,
        meetings=[
            Meeting(r1=1, r2=2, first_time=4),
            Meeting(r1=2, r2=3, first_time=2),
            Meeting(r1=0, r2=1, first_time=2),
            Meeting(r1=0, r2=2, first_time=4)
        ],
        cycles=[
            [2],
            [1, 2],
            [3, 5, 4, 2],
            [6, 5]
        ]
    )


@pytest.fixture
def env3_robots():
    """
    Returns the environment, alongside its robot pair mapping
    :return:
    """
    return DronemEnv(
        num_robots=3,
        init_memory=15,
        max_memory=55,
        meetings=[
            Meeting(r1=1, r2=2, first_time=5),
            Meeting(r1=0, r2=1, first_time=1)
        ],
        cycles=[
            [2],
            [1, 2, 3],
            [4, 3]
        ]
    )


@pytest.fixture
def env3_robots_modified():
    """
        Returns the environment, alongside its robot pair mapping
        :return:
        """
    return DronemEnv(
        num_robots=3,
        init_memory=1,
        max_memory=2,
        meetings=[
            Meeting(r1=1, r2=2, first_time=2),
            Meeting(r1=0, r2=1, first_time=1)
        ],
        cycles=[
            [2],
            [2, 3, 1],
            [4, 3]
        ]
    )
