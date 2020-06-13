"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   21.03.2020 23:47
"""
from typing import List, Any


class State:
    """
    Class for representing a state
    """

    def __init__(self, robots_data: List[int], time: int, positions: List[int]):
        self.robots_data = robots_data
        self.time = time
        self.positions = positions

    def __repr__(self):
        return f"State(robots_data={self.robots_data}, time={self.time}, positions={self.positions})"

    def __eq__(self, other):
        return self.robots_data == other.robots_data and self.time == other.time and self.positions == other.positions


def get_state_from_observation(observation: Any) -> State:
    """
    Function which given an observation returns a state
    :param observation:
    :return:
    """

    return State(
        robots_data=list(observation[:len(observation) // 2]),
        time=observation[len(observation) // 2],
        positions=list(observation[len(observation) // 2 + 1:])
    )


def get_observation_from_state(state: State) -> List[int]:
    """
    Function which given a state returns its observation
    :param state:
    :return:
    """
    return state.robots_data + [state.time] + state.positions
