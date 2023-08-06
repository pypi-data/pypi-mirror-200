import time
import multiprocessing
from multiprocessing import Queue

import eisenmp.eisenmp_worker_loader as loader
import eisenmp.utils.eisenmp_utils as e_utils
import eisenmp.utils.eisenmp_constants as const

multiprocessing.set_start_method('spawn', force=True)


class ProcEnv:
    """Create an environment for worker processes on CPUs.
    All queues shared among processes.
    'maxsize=1' can be altered, should be tested and documented.

    """

    def __init__(self):
        # CPU - process
        self.num_cores = self.core_count_get()
        self.proc_list = []  # join processes at the end
        # Queues
        self.q_max_size = 1
        self.mp_info_q = Queue(maxsize=self.q_max_size)  # fake news and performance data
        self.mp_tools_q = Queue(maxsize=self.q_max_size)  # feeder is thread
        self.mp_print_q = Queue(maxsize=self.q_max_size)  # [!mp blocking!] OMG use sparse, formatted output
        self.mp_input_q = Queue(maxsize=self.q_max_size)  # order lists
        self.mp_output_q = Queue(maxsize=self.q_max_size)  # results and stop confirmation
        self.mp_process_q = Queue(maxsize=self.q_max_size)  # stop order
        self.queue_std_dict = {'mp_info_q': self.mp_info_q,
                               'mp_tools_q': self.mp_tools_q,
                               'mp_print_q': self.mp_print_q,
                               'mp_input_q': self.mp_input_q,
                               'mp_output_q': self.mp_output_q,
                               'mp_process_q': self.mp_process_q}
        self.queue_cust_dict_std = {}  # std dict, val is a q
        self.queue_cust_dict_cat = {}  # custom category, dict in dict
        self.q_lst = []  # all queues in a list, clean up; 'queue_lst_get'

        # Threads - Collect queue grabber
        self.thread_list = []
        self.info_q_thread_name = 'eisenmp_info_q_thread'
        self.input_q_thread_name = 'eisenmp_input_q_thread'
        self.output_q_thread_name = 'eisenmp_output_q_thread'
        self.print_q_thread_name = 'eisenmp_print_q_thread'
        self.tools_q_thread_name = 'eisenmp_tools_q_thread'
        #    ProcInfo
        self.info_proc_info_thread = 'eisenmp_ProcInfo_thread'  # gang
        self.pi = None  # ProcInfo Sub-thread instance thread, start(), cancel()

        # Main switch
        self.all_threads_stop = False  # ends thread loops
        # update
        self.kwargs_env = {}

    def queue_cust_dict_std_create(self, *queue_name_maxsize: tuple):
        """create q, name and maxsize as unpacked list ('blue_q_7', 7)
        - Two queue creator functions. All use tuple to ease unpacking.

        'queue_cust_dict_std_create' - > 'queue_cust_dict_std'
        'queue_cust_dict_category_create' - > 'queue_cust_dict_cat'
        """
        for name, maxsize in queue_name_maxsize:
            self.queue_cust_dict_std[name] = Queue(maxsize=maxsize)

    def queue_cust_dict_category_create(self, *queue_cat_name_maxsize: tuple):
        """('category_1', 'input_q_3', 10)"""
        for cat, name, maxsize in queue_cat_name_maxsize:
            new_dct = {name: Queue(maxsize=maxsize)}
            if cat not in self.queue_cust_dict_cat:
                self.queue_cust_dict_cat[cat] = {}
            self.queue_cust_dict_cat[cat].update(new_dct)

    def queue_lst_get(self):
        """List of qs for shut down msg put in, of ...worker_loader.py
        """
        q_lst = []  # dbg
        for name, q in self.queue_std_dict.items():
            if name == 'mp_print_q':  # else mass prn shutdown messages
                continue
            q_lst.append(q)

        for q in self.queue_cust_dict_std.values():  # custom, std dict
            self.q_lst.append(q)
        for cat_dct in self.queue_cust_dict_cat.values():  # custom, category dict
            for q in cat_dct.values():
                q_lst.append(q)

        self.q_lst.extend(q_lst)
        return self.q_lst

    @staticmethod
    def core_count_get():
        """"""
        num = 1 if not multiprocessing.cpu_count() else multiprocessing.cpu_count() / 2  # hyper thread
        return int(num)

    def kwargs_env_update_custom(self, **kwargs):
        """override default num_cores,
        'queue_lst_get' for worker loader stop msg in all qs
        """
        self.num_cores = kwargs['num_cores'] if 'num_cores' in kwargs and kwargs['num_cores'] else self.core_count_get()
        kwargs.update(self.queue_std_dict)
        kwargs.update(self.queue_cust_dict_std)
        kwargs.update(self.queue_cust_dict_cat)
        all_qs_dict = {'all_qs_lst_dct': self.queue_lst_get()}
        kwargs.update(all_qs_dict)
        return kwargs

    def run_proc(self, **kwargs):  # test with args from caller
        """Create a Process for each CPU core, if `num_proc` None set or not set.
        kwargs dict is updated for worker 'toolbox', reveals all vars and dead ref. avail.
        """
        kwargs = self.kwargs_env_update_custom(**kwargs)
        self.kwargs_env.update(kwargs)

        print(f'\nCreate {self.num_cores} processes.')
        for core in range(self.num_cores):
            print(core, end=" ")
            proc = multiprocessing.Process(target=loader.mp_worker_entry,
                                           kwargs=kwargs)
            proc.start()

            self.proc_list.append(proc)
        self.mp_print_q.put('\n')

    def stop_proc(self):
        """"""
        for proc in range(len(self.proc_list)):
            self.mp_process_q.put(['Simon Says:', const.STOP_PROCESS])

        for process in self.proc_list:
            while process.is_alive():
                time.sleep(.1)

    def end_proc(self):
        """Graceful shutdown join.
        """
        for proc in self.proc_list:
            proc.join()
        print('\tProcesses are down.')

    def stop_thread(self):
        """"""
        for thread in self.thread_list:
            thread.cancel()

    def end_thread(self):
        """Instance and normal threads."""
        e_utils.thread_shutdown_wait(*self.thread_list)
        for t in self.thread_list:
            t.join()
