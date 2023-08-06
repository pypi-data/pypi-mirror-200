import time
import threading
import contextlib
import multiprocessing

import eisenmp.utils.eisenmp_utils as e_utils
import eisenmp.utils.eisenmp_constants as const
from eisenmp.eisenmp_procenv import ProcEnv
from eisenmp.utils.eisenmp_info import ProcInfo


class FunThread(threading.Thread):
    """Thread maker.

    """
    def __init__(self, name, fun_ref, *args, **kwargs):
        super().__init__()
        # thread
        self.name = name
        self.daemon = True
        self.cancelled = False
        # stuff
        self.fun_ref = fun_ref  # no ()
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """_inst.start()"""
        self.fun_ref(*self.args, **self.kwargs)
        self.cancel()

    def cancel(self):
        self.cancelled = True


class QueueCollect(ProcEnv):
    """Queue message collector and printer. Logging from prints.
    Messages in input and output Q have header.
    One can decide later what to do. Alter, or monitor.

    - Output `can` be stored in a box. `store_result` set

    """

    def __init__(self):
        super().__init__()
        # collect box
        self.info_q_box = {}
        self.print_q_box = []
        self.output_q_box = {}  # dict multi thread access, Gang and ProcInfo
        # internal lists
        self.stop_list = []  # proc stop answered, names collector
        self.result_lst_gang = []  # collected findings from procs for this run
        # collect results [baustelle]
        self.e_utilsResult = e_utils.Result()  # interim result calc for long-running tasks, exec(foo), or (bar)

    def enable_q_box_threads(self):
        """Collect Q messages and put em in a box for review, if enabled
        """
        self.enable_print_q()
        self.enable_output_q()

    def enable_info_q(self):
        """Thread for loop."""
        infoQThread = FunThread('eisenmp_InfoQThread', self.info_q_loop)
        infoQThread.start()
        self.thread_list.append(infoQThread)

    def enable_info_thread(self):
        """Shows % done, time left, if fed with an end value"""
        args_inf = [self.info_proc_info_thread,
                    self.mp_print_q,
                    self.info_q_box]
        self.pi = ProcInfo(*args_inf, **self.kwargs_env)  # ProcInfo sits on a subclassed thread
        self.pi.start()  # we cancel() the thread in 'thread_end_join'

    def enable_print_q(self):
        """Thread for loop."""
        printQThread = FunThread('eisenmp_PrintQThread', self.print_q_loop)
        printQThread.start()
        self.thread_list.append(printQThread)

    def enable_output_q(self):
        """Start a thread loop to not block the show.
        Want collect stop confirm worker msg and results, all lists
        """
        outputQThread = FunThread('eisenmp_OutputQThread', self.output_q_loop)
        outputQThread.start()
        self.thread_list.append(outputQThread)

    def print_q_loop(self):
        """Use a Print Q and a thread for formatted printing.

        Use it only sparingly. BLOCKS the whole multiprocessing.
        """
        while 1:
            if self.all_threads_stop:
                break
            try:
                if not self.mp_print_q.empty():
                    with multiprocessing.Lock():
                        msg = self.mp_print_q.get()
                        self.print_q_box.append(msg)
                        print(msg)
            except Exception as e:
                with contextlib.redirect_stdout(None):
                    print(e)

    def output_q_loop(self):
        """Collect list header strings.
        Stop signal strings used to init loops exit.
        Standard dict with num generator for unique keys.
        """
        generator = e_utils.consecutive_number()
        while 1:
            if self.all_threads_stop:
                break
            if not self.mp_output_q.empty():
                msg = self.mp_output_q.get()
                num = next(generator)
                self.output_q_box[num] = msg
                pass

    def info_q_loop(self):
        """Print info or collect statistics from boxed messages.
        Box is a standard dict with num generator for unique keys.
        """
        while 1:
            if self.all_threads_stop:
                break
            generator = e_utils.consecutive_number()
            while not self.all_threads_stop:
                if not self.mp_info_q.empty():
                    msg = self.mp_info_q.get()
                    num = next(generator)
                    self.info_q_box[num] = msg
                    pass

    def enable_view_output_q_box(self):
        """ """
        viewOutputBoxThread = FunThread('eisenmp_viewOutputBoxThread', self.view_output_q_box)
        viewOutputBoxThread.start()
        # can not join() current thread msg

    def view_output_q_box(self):
        """Only lists with header accepted.
        Box is a dictionary.
        """
        outbox = self.output_q_box
        while 1:
            if self.all_threads_stop:
                break

            for idx in range(len(outbox)):
                if type(outbox[idx]) is list:
                    outbox_list = outbox[idx]
                    if const.GOT_RESULT_OUTPUT_Q in outbox_list:  # red list already
                        continue

                    list_header = outbox_list[0]
                    if list_header[:len(const.STOP_CONFIRM)] == const.STOP_CONFIRM:
                        if self.worker_mods_down_ask(list_header):
                            self.print_findings()
                            self.stop_proc()
                            self.end_proc()
                            self.stop_thread()
                            self.end_thread()
                            return

                    if list_header[:len(const.RESULT_HEADER_PROC)] == const.RESULT_HEADER_PROC:
                        result_lst = outbox_list
                        p_result_row = outbox_list[1]
                        if 'store_result' in self.kwargs_env and self.kwargs_env['store_result']:
                            self.e_utilsResult.result_dict_update(list_header, result_lst)
                            self.proc_result_list_findings(p_result_row)

                    outbox_list.append(const.GOT_RESULT_OUTPUT_Q)
            time.sleep(1)  # this thread can slow down bruteforce if too short, [Baustelle] need a trigger here

    def proc_result_list_findings(self, p_result_row):
        """RESULT DICT in utils, collect all results
        Append to result list for print out at finish.
        Add to a dict to monitor results via additional thread during runtime. [baustelle]

        STOP msg was also appended!

        :params: p_result_row: process loop result list row, can be a list in this row
        """
        if const.STOP_MSG in str(p_result_row):
            return

        if type(p_result_row) is list:
            [self.result_lst_gang.append(str(row) + '\n') for row in p_result_row if str(row)]  # internal list
        else:
            self.result_lst_gang.append(str(p_result_row) + '\n')

    def worker_mods_down_ask(self, list_header):
        """All worker MODULES confirm shutdown.

        Worker is using the original name of its process in shut down msg.
        Process IS still running. Worker module entry function returned False.

        :params: list_header: answer of WORKER MODULE to stop request; string with proc id at end
        :returns: None; True if done
        """
        worker_name = list_header[len(const.STOP_CONFIRM):]
        self.stop_list.append(worker_name)
        pending = any([True for proc in self.proc_list if proc.name not in self.stop_list])
        if not pending:
            return True

    def print_findings(self):
        """Condensed result list for this run.
        A thread can sum the results in 'Result' class.
        """
        c_lst = []
        condensed_gen = (line.split('...') for line in list(set(self.result_lst_gang)))
        try:
            c_lst = list(set([tup[2] for tup in condensed_gen]))
        except IndexError:
            c_lst.extend(self.result_lst_gang)

        lbl = self.kwargs_env['result_lbl'] if 'result_lbl' in self.kwargs_env else 'add a "result_lbl" var'
        c_lst.insert(0, f'\n--- Result for [{lbl}]---\n')
        c_lst.append('    --- END ---\n')
        print('\n'.join(c_lst))  # procs down
