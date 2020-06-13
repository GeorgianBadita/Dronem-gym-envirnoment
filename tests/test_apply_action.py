"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   29.03.2020 18:36
"""
from env_interpretation import State
from env_interpretation.action_utils import apply_action_allow_illegal
from env_interpretation.utils import n_from_prod


def test_apply_action_env_3_robots(env3_robots):
    env_data = env3_robots.get_env_metadata()
    env3_robots.reset()
    state = env3_robots.get_current_state()
    action = [61, 0, 0]
    action = n_from_prod(env_data['sets'], action)
    interpreted_action = env3_robots.get_action_from_space(action)
    new_state = apply_action_allow_illegal(state, interpreted_action, env_data['max_memory'], env_data['cycles'])
    assert new_state == State(
        robots_data=[21, 9, 15],
        time=2,
        positions=[2, 2, 3]
    )
    action = [61, 0, 0]
    action = n_from_prod(env_data['sets'], action)
    interpreted_action = env3_robots.get_action_from_space(action)
    assert apply_action_allow_illegal(state, interpreted_action, env_data['max_memory'], env_data['cycles']) == new_state



def test_apply_action_test_4_env(env4_robots):
    env_data = env4_robots.get_env_metadata()
    env4_robots.reset()
    state = env4_robots.get_current_state()
    state.time = 8
    action = [19, 16, 0, 0, 0, 18]
    action = n_from_prod(env_data['sets'], action)
    interpreted_action = env4_robots.get_action_from_space(action)
    new_state = apply_action_allow_illegal(state, interpreted_action, env_data['max_memory'], env_data['cycles'])
    assert new_state == State(
        robots_data=[15, 6, 12, 7],
        time=9,
        positions=[2, 2, 5, 5]
    )

    action = [26, 16, 0, 0, 0, 22]
    action = n_from_prod(env_data['sets'], action)

    interpreted_action = env4_robots.get_action_from_space(action)
    new_state = apply_action_allow_illegal(state, interpreted_action, env_data['max_memory'], env_data['cycles'])
    assert new_state == State(
        robots_data=[11, 10, 9, 10],
        time=9,
        positions=[2, 2, 5, 5]
    )

