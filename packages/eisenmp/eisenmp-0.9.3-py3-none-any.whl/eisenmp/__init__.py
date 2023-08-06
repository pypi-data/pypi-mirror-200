"""eisenmp

A Python ``multiprocess, multi CPU`` module.
An example function cracks a game quest.

    ::

    Inheritance - proc: ProcEnv -> QueueCollect -> Mp
        Create Queue/Process -> Collect messages in boxes -> Manage, feed

    Thread names are in ProcEnv:
        QueueCollect [print_q, output_q, input_q, tools_q, info_q],
        GhettoGang [view_output_q_box, tools_q feeder],
        [ProcInfo]

"""
import time
import threading

import eisenmp.eisenmp_q_coll as coll
import eisenmp.eisenmp_procenv as procenv
import eisenmp.utils.eisenmp_utils as e_utils
import eisenmp.utils.eisenmp_constants as const
from eisenmp.eisenmp_q_coll import QueueCollect


class Mp(QueueCollect):
    """MultiProcessManager.

    """

    def __init__(self):
        super().__init__()
        self.kwargs = None

    def start(self, **kwargs):
        """enable Processes and eisenmp worker threads.
        """
        self.all_threads_stop = False  # frequent calls without exit, see bruteforce
        self.kwargs = kwargs
        self.run_proc(**kwargs)

        self.enable_q_box_threads()  # [Baustelle] some q are collected in boxes, 'output', 'print' for later review
        self.enable_view_output_q_box()  # search worker stop msg and collect result if 'store_result' is set

        self.enable_info_q()  # never disable, else sender blocks, nobody consumes from q
        if 'enable_info' in kwargs and kwargs['enable_info']:
            self.enable_info_thread()  # collect worker send nums from info box and shows % and ETA
        return

    def run_q_feeder(self, **kwargs):
        """Threaded instance, run multiple q_feeder, called by manager of worker
        """
        self.kwargs.update(kwargs)  # upd boss kwargs with generator, queues and header_msg
        threading.Thread(name='eisenmp_q_feeder',  # better than class thread here, no overlap, interesting.
                         target=self.q_feeder(),
                         ).start()

    def q_feeder(self):
        """Chunk list producer of generator input.

        - We need a generator to make chunks of whatever. Put chunks in list rows for transport. Numbers, str, dicts ...
        - A ticket is attached as header, to identify the workload (list chunks).
        - We stamp the lists with a serial number to rebuild the modified results in the right order, if needed.
        """
        kw = self.kwargs
        generator = kw['generator']  # no generator, crash for sure
        num_rows = kw['num_rows'] if 'num_rows' in kw and kw['num_rows'] else const.NUM_ROWS
        header_msg = kw['header_msg'] if 'header_msg' in kw and kw['header_msg'] else const.HEADER_MSG
        feeder_input_q = kw['feeder_input_q'] if 'feeder_input_q' in kw else self.mp_input_q

        start = time.perf_counter()
        num_gen = e_utils.consecutive_number()
        while 1:
            if self.all_threads_stop:
                break
            chunk_lst = create_transport_ticket(num_gen, header_msg)
            for _ in range(num_rows):
                try:
                    chunk_lst.append(next(generator))
                except StopIteration:
                    chunk_lst.append(const.STOP_MSG)  # signal stop to one worker module, worker module 'loader' to many
                    self.mp_print_q.put(f'\n\tgenerator empty, '
                                        f'run time iterator {round((time.perf_counter() - start))} seconds\n')
                    feeder_input_q.put(chunk_lst)
                    return

            feeder_input_q.put(chunk_lst)


def create_transport_ticket(num_gen, header_msg=None):
    """Semicolon to split easy.
    """
    header_msg = header_msg if header_msg else const.HEADER_MSG
    serial_num = f';_ID_;{str(next(num_gen))}'
    return [header_msg + serial_num]
