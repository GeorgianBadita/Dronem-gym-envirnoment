"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   21.03.2020 00:58
"""

from env_interpretation import Meeting
from env_interpretation.meeting import get_valid_meetings


def test_get_meetings_4_robots(env4_robots):
    env_data = env4_robots.get_env_metadata()
    cycles_length = [len(x) for x in env_data['cycles']]

    meetings_at_0 = get_valid_meetings(0, env_data['meetings'], cycles_length)
    assert meetings_at_0 == []
    meetings_at_2 = get_valid_meetings(2, env_data['meetings'], cycles_length)
    assert meetings_at_2 == [
        Meeting(r1=2, r2=3, first_time=2),
        Meeting(r1=0, r2=1, first_time=2)
    ]
    assert get_valid_meetings(5, env_data['meetings'], cycles_length) == []
    meetings_at_8 = get_valid_meetings(8, env_data['meetings'], cycles_length)

    assert set(meetings_at_8) == {Meeting(r1=1, r2=2, first_time=4),
                                  Meeting(r1=0, r2=1, first_time=2),
                                  Meeting(r1=0, r2=2, first_time=4)
                                  }

    assert get_valid_meetings(9, env_data['meetings'], cycles_length) == []

    assert set(get_valid_meetings(14, env_data['meetings'], cycles_length)) == {
        Meeting(r1=2, r2=3, first_time=2),
        Meeting(r1=0, r2=1, first_time=2)
    }


def test_get_meetings_3_robots(env3_robots):
    env_data = env3_robots.get_env_metadata()
    cycles_length = [len(x) for x in env_data['cycles']]

    assert get_valid_meetings(0, env_data['meetings'], cycles_length) == []
    assert get_valid_meetings(1, env_data['meetings'], cycles_length) == [
        Meeting(r1=0, r2=1, first_time=1)
    ]
    assert get_valid_meetings(23, env_data['meetings'], cycles_length) == [
        Meeting(r1=1, r2=2, first_time=5)] == get_valid_meetings(5, env_data['meetings'], cycles_length)
