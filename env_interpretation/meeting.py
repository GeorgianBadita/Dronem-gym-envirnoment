"""
    @author: Badita Marin-Georgian
    @email:  geo.badita@gmail.com
    @date:   21.03.2020 00:46
"""
from collections import namedtuple
from typing import List

from env_interpretation.utils import lcm

Meeting = namedtuple("Meeting", ['r1', 'r2', 'first_time'])


def get_valid_meetings(time: int, possible_meetings: List[Meeting], cycle_lengths: List[int]) -> List[Meeting]:
    """
    Function which returns all possible meetings at a given time
    :return:
    """

    return [
        meeting
        for meeting in possible_meetings
        if time == meeting.first_time or (time > meeting.first_time
                                          and ((time - meeting.first_time) /
                                               lcm(cycle_lengths[meeting.r1], cycle_lengths[meeting.r2])).is_integer())
    ]
