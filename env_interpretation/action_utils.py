"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   19.03.2020 23:41
"""
from collections import namedtuple
from typing import List

from env_interpretation import State
from copy import deepcopy

Exchange = namedtuple('Exchange', ['r1', 'r2', 'quant'])


def apply_action_allow_illegal(state: State, interpreted_action: List[Exchange], max_memory,
                               cycles: List[List[int]]) -> State:
    """
    Function which applies an action to a state
    :param state: current state
    :param interpreted_action: action to be applied
    :param max_memory: robot's maximum memory
    :param cycles - robot's cycles
    :return: new state
    """
    state = State(
        robots_data=deepcopy(state.robots_data),
        time=state.time,
        positions=deepcopy(state.positions)
    )
    curr_index = [cycles[i].index(state.positions[i]) for i in range(len(state.positions))]
    for exchange in interpreted_action:

        if exchange.r1 == 0 and exchange.quant > 0:
            continue
        if exchange.r1 == 0 and exchange.quant < 0 and state.robots_data[exchange.r2] + exchange.quant >= 0:
            state.robots_data[exchange.r1] -= exchange.quant
            state.robots_data[exchange.r2] += exchange.quant
            continue
        if exchange.quant > 0 and state.robots_data[exchange.r2] + exchange.quant > max_memory or exchange.quant < 0 \
                and state.robots_data[exchange.r1] - exchange.quant > max_memory:
            continue
        if exchange.quant > 0 <= state.robots_data[exchange.r1] - exchange.quant:
            state.robots_data[exchange.r1] -= exchange.quant
            state.robots_data[exchange.r2] += exchange.quant

        elif exchange.quant < 0 <= state.robots_data[exchange.r2] + exchange.quant:
            state.robots_data[exchange.r1] -= exchange.quant
            state.robots_data[exchange.r2] += exchange.quant
    for i in range(len(state.positions)):
        if curr_index[i] < len(cycles[i]) - 1:
            state.positions[i] = cycles[i][curr_index[i] + 1]
        else:
            state.positions[i] = cycles[i][0]
    state.time = state.time + 1
    return state


def apply_action_only_increase_time_move_robots(state: State, interpreted_action: List[Exchange], max_memory,
                                                cycles: List[List[int]]) -> State:
    state = State(
        robots_data=deepcopy(state.robots_data),
        time=state.time,
        positions=deepcopy(state.positions)
    )
    curr_index = [cycles[i].index(state.positions[i]) for i in range(len(state.positions))]
    for i in range(len(state.positions)):
        if curr_index[i] < len(cycles[i]) - 1:
            state.positions[i] = cycles[i][curr_index[i] + 1]
        else:
            state.positions[i] = cycles[i][0]
    state.time = state.time + 1
    return state
