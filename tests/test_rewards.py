"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   24.03.2020 23:44
"""

from env_interpretation import State, settings

from env_interpretation.reward_utils import OneMinusOneRewardGiverAllowIllegal
from env_interpretation.utils import n_from_prod


def test_one_minus_one_reward_bad_env_3(env3_robots):
    env_data = env3_robots.get_env_metadata()
    action = [15, 20, 56]
    action = n_from_prod(env_data['sets'], action)
    interpreted_action = env3_robots.get_action_from_space(action)
    reward_giver = OneMinusOneRewardGiverAllowIllegal()
    assert reward_giver.give_reward(State([15, 20, 1], 5, None),
                                    interpreted_action, env_data['meetings'],
                                    env_data['cycle_lengths'],
                                    env_data['max_memory']) == 2 * settings.REWARD_FOR_INVALID_MEETING - 1


def test_one_minus_one_reward_good_env_3(env3_robots):
    env_data = env3_robots.get_env_metadata()
    action = [57, 0, 0]
    action = n_from_prod(env_data['sets'], action)
    interpreted_action = env3_robots.get_action_from_space(action)
    reward_giver = OneMinusOneRewardGiverAllowIllegal()

    assert reward_giver.give_reward(State([2, 2, 0], 10, None),
                                    interpreted_action, env_data['meetings'],
                                    env_data['cycle_lengths'], env_data['max_memory']) == 1

    action = [58, 0, 0]
    action = n_from_prod(env_data['sets'], action)
    interpreted_action = env3_robots.get_action_from_space(action)

    assert reward_giver.give_reward(State([0, 0, 0], 10, None),
                                    interpreted_action, env_data['meetings'],
                                    env_data['cycle_lengths'], env_data['max_memory']) == settings.REWARD_FOR_INVALID_TRANSFER


def test_one_minus_one_reward_bad_env_4(env4_robots):
    env_data = env4_robots.get_env_metadata()
    action = [1, 2, 20, 15, 13, 28]
    action = n_from_prod(env_data['sets'], action)
    # {(r0 -> r1: 1), (r0 -> r2: 2), (r3 -> r0: 5),
    # (r1 -> r2: 15), (r1 -> r3: 13), (r3 -> r2: 13)}
    interpreted_action = env4_robots.get_action_from_space(action)
    reward_giver = OneMinusOneRewardGiverAllowIllegal()

    assert reward_giver.give_reward(
        State([10, 10, 10, 10], 8, None),
        interpreted_action, env_data['meetings'],
        env_data['cycle_lengths'],
        env_data['max_memory']) == 5 * settings.REWARD_FOR_INVALID_MEETING + settings.REWARD_FOR_INVALID_TRANSFER

    assert reward_giver.give_reward(
        State([0, 0, 0, 0], 8, None),
        interpreted_action, env_data['meetings'],
        env_data['cycle_lengths'],
        env_data['max_memory']) == 5 * settings.REWARD_FOR_INVALID_MEETING + settings.REWARD_FOR_INVALID_TRANSFER

    action = [0] * (env_data['num_robots'] * (env_data['num_robots'] - 1) // 2)
    action = n_from_prod(env_data['sets'], action)
    interpreted_action = env4_robots.get_action_from_space(action)
    assert reward_giver.give_reward(
        State([0, 0, 0, 0], 8, None),
        interpreted_action, env_data['meetings'],
        env_data['cycle_lengths'],
        env_data['max_memory']) == 0


def test_one_minus_one_reward_good_env_4(env4_robots):
    env_data = env4_robots.get_env_metadata()
    action = [17, 0, 0, 0, 0, 13]
    action = n_from_prod(env_data['sets'], action)
    # {(r1 -> r0: 2), ,
    # (r2 -> r3: 13)}
    interpreted_action = env4_robots.get_action_from_space(action)
    reward_giver = OneMinusOneRewardGiverAllowIllegal()

    assert reward_giver.give_reward(
        State([10, 10, 15, 0], 10, None),
        interpreted_action, env_data['meetings'],
        env_data['cycle_lengths'],
        env_data['max_memory']) == 0

    assert reward_giver.give_reward(
        State([10, 10, 10, 10], 10, None),
        interpreted_action, env_data['meetings'],
        env_data['cycle_lengths'],
        env_data['max_memory']) == settings.REWARD_FOR_INVALID_TRANSFER + 1

    action = [25, 0, 0, 0, 0, 13]
    action = n_from_prod(env_data['sets'], action)

    # {(r1 -> r0: 10), ,
    # (r2 -> r3: 13)}
    interpreted_action = env4_robots.get_action_from_space(action)
    assert reward_giver.give_reward(
        State([10, 10, 15, 0], 10, None),
        interpreted_action, env_data['meetings'],
        env_data['cycle_lengths'],
        env_data['max_memory']) == 0
