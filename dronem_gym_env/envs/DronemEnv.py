"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   11.03.2020 22:54
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

import gym
import numpy as np
from gym import spaces

from env_interpretation import Meeting
from env_interpretation import settings
from env_interpretation.action_utils import Exchange
from env_interpretation.action_utils import apply_action_allow_illegal
from env_interpretation.action_utils import apply_action_only_increase_time_move_robots
from env_interpretation.lazy_cartesian_product import LazyCartesianProduct
from env_interpretation.meeting import get_valid_meetings
from env_interpretation.reward_utils import OneMinusOneRewardGiverNotAllowIllegal
from env_interpretation.state_utils import State
from env_interpretation.state_utils import get_observation_from_state
from env_interpretation.state_utils import get_state_from_observation
from env_interpretation.utils import check_if_done
from env_interpretation.utils import n_from_prod


class DronemEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, num_robots: int = None, max_memory: int = None, init_memory: int = None,
                 meetings: List[Meeting] = (), cycles: List[List[int]] = ()):
        """
        Constructor for Dronem environment, assumes R0 is sink
        :param num_robots: number of robots
        :param max_memory: maximum memory
        :param init_memory: initial data in robot's memory
        :param meetings: list with all possible meetings (in every meeting r1 < r2 for consistency)
        :param cycles: cycles patrolled by each robot

        Env Description:
            A fleet of robots patrols a set of cycles, each robot has an initial quantity of data
            Two or more robots can meet at some point, a robot R1 can give data to robot R2 if it has data
            and R2 has enough memory to store the new data

        Actions:
            Type: Discrete((2 * max_memory + 1) ^ n(n - 1)/2) n - number of robots
            Basically if for every ordered pair of robots we have the quantity of data ri gives to rj, i < j.
            If the value is <= max_memory we have transfer from ri to rj, else if the value is > max_memory
            we have transfer from rj to ri
            We can have this space to be discrete because we have a LazyCartesianProduct class, which gives the nth element
            of the cartesian product in almost O(1)
            Num             Action
            [0, 0, ... 0]   [Exchange(r0, r1, quant=0), Exchange(r0, r2, quant = 0), .., Exchange(rn-1, rn, quant=0]
            [i, j, ... x]   [Exchange(r0, r1, quant=i), Exchange(r0, r2, quant = j), ..,
            Exchange(r_{n-1}, r_{n}, quant=max_memory - x) (if x > max_memory)

        Observation:
            Type:
        """
        self.__INF = 10 ** 9
        self.__num_robots = num_robots
        self.__max_memory = max_memory
        self.__init_memory = init_memory
        self.__meetings = meetings
        self.__cycles = cycles
        self.__robots_mem = [self.__init_memory] * self.__num_robots
        # self.__reward_class = OneMinusOneRewardGiverAllowIllegal()
        self.__reward_class = OneMinusOneRewardGiverNotAllowIllegal()
        self.__action_apply = apply_action_allow_illegal
        self.__cycles_lengths = [len(cycle) for cycle in self.__cycles]
        self.__action_mapping = [
            (i, j) for i in range(self.__num_robots - 1)
            for j in range(i + 1, self.__num_robots)
            if i < j
        ]
        self.__sets = [[x for x in range(0, 2 * self.__max_memory + 1)] for _ in range(
            self.__num_robots * (self.__num_robots - 1) // 2
        )]
        self.lazy_action_get = LazyCartesianProduct(self.__sets)
        self.action_space = spaces.Discrete(self.lazy_action_get.max_size)
        self.observation_space = spaces.MultiDiscrete(
            [self.__INF] +  # how much data can the sink store
            [max_memory] * (num_robots - 1) +  # how much data each robot holds,
            [self.__INF] +  # timestamp
            [max(cycle) for cycle in self.__cycles]  # robots positions
        )
        self.state = None
        self.__state_action = None

    def get_current_state(self) -> State:
        """
        Return current interpreted state of the environment
        """
        return get_state_from_observation(self.state)

    def get_env_metadata(self) -> Dict[str, Any]:
        """
        Function which returns information about the environment
        """

        return {
            'num_robots': self.__num_robots,
            'max_memory': self.__max_memory,
            'init_memory': self.__init_memory,
            'meetings': self.__meetings,
            'cycles': self.__cycles,
            'cycle_lengths': self.__cycles_lengths,
            'sets': self.__sets,
            'worst_reward': settings.REWARD_FOR_INVALID_ACTION,
            'max_steps': settings.MAXIMUM_NUM_ITER
        }

    def select_valid_action(self) -> List[int]:
        """
        Function which selects a valid action for the current state
        :return: int (action index)
        """
        interpreted_state = get_state_from_observation(self.state)
        # print(interpreted_state)
        tmp_sets = []
        for i in range(self.__num_robots * (self.__num_robots - 1) // 2):
            r1, r2 = self.__action_mapping[i]
            rng = list(range(interpreted_state.robots_data[r1] + 1)) + list(
                range(self.__max_memory + 1, self.__max_memory + 1 + interpreted_state.robots_data[r2]))
            tmp_sets.append(rng)

        tmp_lazy_action_get = LazyCartesianProduct(tmp_sets)
        tmp_action = tmp_lazy_action_get.get_nth_element(np.random.randint(0, tmp_lazy_action_get.max_size))
        valid_meetings = get_valid_meetings(interpreted_state.time, self.__meetings, self.__cycles_lengths)
        # print("VALID MEETINGS: " + str(valid_meetings))
        pair_list = set([(x.r1, x.r2) for x in valid_meetings])
        # print("TMP_ACTION_BEFORE" + str(tmp_action))
        for i in range(len(self.__action_mapping)):
            r1, r2 = self.__action_mapping[i]
            if (r1, r2) not in pair_list:
                tmp_action[i] = 0
            elif r1 == 0:
                if interpreted_state.robots_data[r2] == 0:
                    tmp_action[i] = 0
                else:
                    tmp_action[i] = np.random.randint(self.__max_memory + 1,
                                                      self.__max_memory + 1 + interpreted_state.robots_data[r2])
        # print("TMP_ACTION_AFTER" + str(tmp_action))
        return tmp_action

    def step(self, action: int) -> Tuple[np.array, float, bool, Dict]:
        # check if the action is in the action space
        if not isinstance(action, list):
            action = int(action)
        else:
            assert self.action_space.contains(action), f'{action}, {type(action)} invalid'
            action = n_from_prod(self.__sets, action)
        interpreted_state = get_state_from_observation(self.state)  # convert observation to interpreted state
        interpreted_action = self.get_action_from_space(action)
        self.__state_action = interpreted_action
        reward = self.__reward_class.give_reward(interpreted_state, interpreted_action,
                                                 self.__meetings, self.__cycles_lengths, self.__max_memory)

        if reward == settings.REWARD_FOR_INVALID_ACTION:
            # new_state = interpreted_state
            new_state = apply_action_only_increase_time_move_robots(interpreted_state,
                                                                    interpreted_action,
                                                                    self.__max_memory,
                                                                    self.__cycles)
        else:
            new_state = self.__action_apply(interpreted_state, interpreted_action, self.__max_memory, self.__cycles)

        self.state = np.array(get_observation_from_state(new_state))
        return self.state, reward / 1000000, check_if_done(new_state,
                                                           settings.MAXIMUM_NUM_ITER), {}

    def reset(self):
        self.state = np.array(get_observation_from_state(
            State(
                robots_data=[self.__init_memory] * self.__num_robots,
                time=1,
                positions=[x[0] for x in self.__cycles]
            )
        ))
        return self.state

    def render(self, mode='human', close=False):
        print(f"{self.state}, {self.__state_action}")

    def get_action_from_space(self, num_action: int) -> List[Exchange]:
        """
        Function to get the real action interpretation from the action space
        :param num_action: action number
        :return: List of exchanges
        """
        action = self.lazy_action_get.get_nth_element(num_action)
        action = [x if x <= self.__max_memory else self.__max_memory - x for x in action]

        return [Exchange(r1=self.__action_mapping[i][0], r2=self.__action_mapping[i][1], quant=action[i])
                for i in range(len(action))]
