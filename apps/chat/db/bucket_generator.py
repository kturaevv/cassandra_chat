""" Module for 3 minute session id generation. """

import datetime
import random

from uuid import UUID
from functools import lru_cache


def generate_session_id(timestamp) -> int:
    vals = _get_timestamp_values(timestamp)
    return _generate_session_timeuuid(*vals)
    
def _get_session_start_minute(minute) -> int:
    """ Returns 3 minute session start time for unique id generation. """

    if minute % 3 == 0:
        return minute
    elif (minute - 1) % 3 == 0:
        return minute - 1
    else:
        return minute - 2
    
def _get_timestamp_values(timestamp: float) -> tuple:
    _now = datetime.datetime.fromtimestamp(timestamp)
    return _now.year, _now.month, _now.day, _now.hour, _get_session_start_minute(_now.minute)

@lru_cache(maxsize=1)
def _generate_session_timeuuid(*args: int) -> int:
    """
        Since we know the ranges, it is possible to tailor session id generation
        within 32 bit int representation (int).

        arg     |     arg range    |   bit range    | max value    
        --------------------------------------------------------   
        year:   |   range(1, 4096) |    12-bit      |   4096
        month:  |   range(1 - 12)  |    4-bit       |   16
        day:    |   range(0 - 31)  |    5-bit       |   32
        hour:   |   range(0 - 23)  |    5-bit       |   32
        minute: |   range(0 - 59)  |    6-bit       |   64
        --------------------------------------------------------   
        Result:                     32-bit integer

    Note: There is 32-bit of additional space for further customizetion if needed.
    """
    if len(args) != 5:
        raise ValueError(
            "Input should be 5 value tuple: year - month - day - hour - minute"
            )
            
    (year, month, day, hour, minute) = args

    if not 0 <= year < 1 << 12:
        raise ValueError('field 1 out of range (need a 16-bit value)')
    if not 0 <= month < 1 << 4:
        raise ValueError('field 2 out of range (need a 8-bit value)')
    if not 0 <= day < 1 << 5:
        raise ValueError('field 3 out of range (need a 8-bit value)')
    if not 0 <= hour < 1 << 5:
        raise ValueError('field 4 out of range (need an 8-bit value)')
    if not 0 <= minute < 1 << 6:
        raise ValueError('field 5 out of range (need an 8-bit value)')
    
    int_ = ( year << 20 | month << 16 | day << 11 | hour << 6 | minute)
    return int_

if __name__ == "__main__":
    ts = datetime.datetime.now().timestamp()
    session_id = generate_session_id(ts)
    assert type(session_id) == int
    assert len(bin(session_id)) - 2 <= 32