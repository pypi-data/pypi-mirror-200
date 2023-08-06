import time
import threading
from collections import defaultdict


class Result:
    """Finest results only here.
    Can save number stuff, not response chunks, or we crash

    """

    def __init__(self):
        self._result_dict = defaultdict(list)  # threads can read/write dict

    @property
    def result_dict(self):
        return self._result_dict

    @result_dict.setter
    def result_dict(self, update):
        self._result_dict = update

    @result_dict.deleter
    def result_dict(self):
        del self._result_dict

    def result_dict_update(self, key, value):
        self._result_dict[key].append(value)


def consecutive_number():
    """Want a stamp on each list header.
    Used for Queue messages get() and put in box_dict[num] = msg
    Can rebuild original order if worker puts result in a list
    with same num as order list.
    """
    idx = 0
    while 1:
        yield idx
        idx += 1


def thread_shutdown_wait(*threads):
    """We return if none of the thread names are listed anymore.
    Blocks!

    :params: *threads: arbitrary list of thread names
    """
    busy = True
    while busy:
        names_list = [thread.name for thread in threading.enumerate()]
        busy = True if any([True for thread in threads if thread in names_list]) else False
        time.sleep(.1)
