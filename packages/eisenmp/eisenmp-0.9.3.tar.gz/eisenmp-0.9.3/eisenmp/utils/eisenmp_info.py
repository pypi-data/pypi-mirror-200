import time
import threading

import eisenmp.utils.eisenmp_constants as constants


class ProcInfo(threading.Thread):
    """Thread; start(), cancel()
    Brute Force uses factorial as target to calculate.
    Prime uses 'range_num' of num generator as target.
        List rows done are the current state
    estimated time of arrival, ETA.
    So far.

    We sit on the QueueCollect and loop over the collected items in a list or dict (box).
    instantiated by GhettoGang

    """

    def __init__(self, name, print_q, info_q_box, **kwargs):
        super().__init__()
        # thread
        self.name = name
        self.daemon = True
        self.cancelled = False
        # info
        self.perf_dict_eta = {}
        self.info_shutdown = False
        self.print_q = print_q
        self.info_q_box = info_q_box  # dict
        self.info_td_max = kwargs['info_td_max'] if 'info_td_max' in kwargs else None
        self.info_td_exec = kwargs['info_td_exec'] if 'info_td_exec' in kwargs else None

    def run(self):
        """feed init args instead of method args"""
        self.performance_coll()

    def cancel(self):
        self.info_shutdown = True
        self.cancelled = True

    def arrival_eta(self):
        """Calc ETA and percent done.
        """
        target = self.perf_dict_eta['target']
        current = self.perf_dict_eta['rows_done']
        start_time = self.perf_dict_eta['proc_start']

        if target and current:
            this_percent = current / target
            this_time = round((time.perf_counter() - start_time))

            est_arrival = this_time / this_percent
            time_left = est_arrival - this_time
            show_time = round(time_left, 1)
            show_percent = round((this_percent * 100), 1)
            return show_percent, show_time

    def perf_count_eta(self, info_box):
        """
        """
        for idx in range(len(info_box)):
            if idx in info_box.keys():
                if type(info_box[idx]) is list:

                    list_header = info_box[idx][0]
                    if list_header[:14] == constants.PERF_HEADER_ETA:
                        a_num = int(info_box[idx][1])
                        if self.info_td_max:
                            self.perf_dict_eta['target'] = self.info_td_max
                            if self.info_td_exec:
                                exec(self.info_td_exec)
                            else:
                                self.perf_dict_eta['rows_done'] += a_num  # ETA
                        info_box[idx] = None

    def perf_count_print_eta(self):
        """
        """
        if self.arrival_eta():
            percent, sec_left = self.arrival_eta()
            if 3_600 <= sec_left <= 86_400:
                msg_time = f' "{round(sec_left / 3_600, 1)}" hours left'
            elif sec_left >= 86_400:
                msg_time = f' "{round(sec_left / 86_400, 1)}" days left'
            else:
                msg_time = f' "{round(sec_left, 1)}" seconds left'

            msg = f'\n\t[ "{percent}%" done, {msg_time} ]\n'
            self.print_q.put(msg)

    def performance_coll(self):
        """Print time and percent.
        Loops forever if no search str or performance info.
        """
        self.perf_dict_eta = {'target': 0,
                              'rows_done': 0,
                              'proc_start': time.perf_counter()}
        info_box = self.info_q_box
        while not self.info_shutdown:  # self.perf_dict_eta['rows_done']
            self.perf_count_eta(info_box)
            self.perf_count_print_eta()
            for _ in range(40):
                if self.info_shutdown:
                    return
                time.sleep(.1)


if __name__ == '__main__':
    pass
    # ProcInfo()
