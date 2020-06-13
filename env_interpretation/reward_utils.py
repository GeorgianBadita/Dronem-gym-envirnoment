"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   20.03.2020 00:45
"""
from typing import List

from env_interpretation import Exchange, Meeting, State
from env_interpretation.meeting import get_valid_meetings
from env_interpretation import settings
from copy import deepcopy

from env_interpretation.utils import check_if_done


class RewardGiver:
    """
    Class for reward giver (used to implement more than One types of rewards)
    """

    def give_reward(self, state: State, interpreted_action: List[Exchange],
                    meetings: List[Meeting], cycles_lengths: List[int], max_memory: int) -> float:
        """
        Function which gives a reward based on state, action, possible meetings, cycle_lengths and
        the maximum memory
        """
        raise NotImplementedError("Method give_reward from RewardGiver not implemented")


class OneMinusOneRewardGiverAllowIllegal(RewardGiver):
    """
    Simple -1 1 reward giver
    """

    def give_reward(self, state: State, interpreted_action: List[Exchange],
                    meetings: List[Meeting], cycles_lengths: List[int], max_memory: int):
        state_cpy = State(deepcopy(state.robots_data), state.time, deepcopy(state.positions))

        reward = 0
        valid_meetings = get_valid_meetings(state.time, meetings, cycles_lengths)
        r1_r2_meeting_list = [[x.r1, x.r2] for x in valid_meetings]
        for exchange in interpreted_action:
            r1 = exchange.r1
            r2 = exchange.r2
            if [r1, r2] not in r1_r2_meeting_list and exchange.quant != 0:
                reward += settings.REWARD_FOR_INVALID_MEETING
            elif r1 == 0 and exchange.quant > 0:
                reward += settings.REWARD_FOR_INVALID_MEETING
            else:
                if r1 == 0 and exchange.quant < 0 and state_cpy.robots_data[r2] + exchange.quant >= 0:
                    reward += 1
                    state_cpy.robots_data[r1] -= exchange.quant
                    state_cpy.robots_data[r2] += exchange.quant
                    continue
                if exchange.quant < 0 and (state_cpy.robots_data[r1] - exchange.quant > max_memory or
                                           state_cpy.robots_data[r2] + exchange.quant < 0):
                    reward += settings.REWARD_FOR_INVALID_TRANSFER
                elif exchange.quant > 0 and (state_cpy.robots_data[r2] + exchange.quant > max_memory or
                                             state_cpy.robots_data[r1] - exchange.quant < 0):
                    reward += settings.REWARD_FOR_INVALID_TRANSFER
                elif r1 == 0 and exchange.quant < 0:
                    state_cpy.robots_data[r1] -= exchange.quant
                    state_cpy.robots_data[r2] += exchange.quant
                    reward += 1
                elif exchange.quant != 0:
                    state_cpy.robots_data[r1] -= exchange.quant
                    state_cpy.robots_data[r2] += exchange.quant
                    reward += -1
        return reward


class OneMinusOneRewardGiverNotAllowIllegal(RewardGiver):
    """
    Simple -1 1 reward giver
    """

    def give_reward(self, state: State, interpreted_action: List[Exchange],
                    meetings: List[Meeting], cycles_lengths: List[int], max_memory: int):
        state_cpy = State(deepcopy(state.robots_data), state.time, deepcopy(state.positions))
        exchanges = [x.quant for x in interpreted_action]
        valid_meetings = get_valid_meetings(state.time, meetings, cycles_lengths)

        if max(exchanges) == 0 == min(exchanges):
            return int(settings.REWARD_FOR_INVALID_ACTION * 2 / 3)
        reward = 0
        r1_r2_meeting_list = [[x.r1, x.r2] for x in valid_meetings]
        for exchange in interpreted_action:
            r1 = exchange.r1
            r2 = exchange.r2
            if [r1, r2] not in r1_r2_meeting_list and exchange.quant != 0:
                return settings.REWARD_FOR_INVALID_ACTION
            elif r1 == 0 and exchange.quant > 0:
                return settings.REWARD_FOR_INVALID_ACTION
            else:
                if r1 == 0 and exchange.quant < 0 and state_cpy.robots_data[r2] + exchange.quant >= 0:
                    reward += -exchange.quant
                    state_cpy.robots_data[r1] -= exchange.quant
                    state_cpy.robots_data[r2] += exchange.quant
                    continue
                if exchange.quant < 0 and (state_cpy.robots_data[r1] - exchange.quant > max_memory or
                                           state_cpy.robots_data[r2] + exchange.quant < 0):
                    return settings.REWARD_FOR_INVALID_ACTION
                elif exchange.quant > 0 and (state_cpy.robots_data[r2] + exchange.quant > max_memory or
                                             state_cpy.robots_data[r1] - exchange.quant < 0):
                    return settings.REWARD_FOR_INVALID_ACTION
                elif r1 == 0 and exchange.quant < 0:
                    state_cpy.robots_data[r1] -= exchange.quant
                    state_cpy.robots_data[r2] += exchange.quant
                    reward += abs(exchange.quant) * 1000
                elif exchange.quant != 0:
                    state_cpy.robots_data[r1] -= exchange.quant
                    state_cpy.robots_data[r2] += exchange.quant
                    reward += 1000

        if check_if_done(state_cpy):
            return settings.END_ENVIRONMENT
        return reward
