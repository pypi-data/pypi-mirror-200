"""Worker and mates module loader.
Mate worker modules MUST call a threaded start_function(),
else we hang. See watchdog.

"""

import os
import sys
import multiprocessing as mp

import eisenmp.utils.eisenmp_constants as const


class ToolBox:
    """Storage box for a Single Worker Process.

    """
    def __init__(self):
        self.mp_info_q = None  # performance data, or other
        self.mp_tools_q = None  # data too big to send with every list to worker
        self.mp_print_q = None  # formatted screen output with multiprocessor lock(), use sparse
        self.mp_input_q = None
        self.mp_output_q = None
        self.mp_process_q = None  # proc shutdown msg's
        self.next_lst = None  # input_q, next list from your generator -> Ghetto is iterator, list creator
        self.worker_id = None  # name id from Process name
        self.worker_pid = None  # process pid
        self.worker_name = None  # stop confirmations collected by GhettoGang and send shutdown signal to program
        self.header_msg = None  # list header, attached for every list
        self.multi_tool = None  # tools_q, can be any prerequisite object for a module
        self.stop_msg = None  # all q, not mp_print_q, if Boss StopIteration is raised, or this wrk informs other worker
        self.stop_confirm = ''  # output_q, GhettoGang collects msg to send shutdown signal to program
        self.result_header_proc = ''  # identify proc result in output_q_box
        self.perf_header_eta = None  # 'PROC_PERF_ETA_'
        self.perf_current_eta = None  # list rows done or other count
        self.kwargs = None


def module_path_load(file_path):
    """Imports the module from path and returns it in the env.
    """
    path, f_name = os.path.split(file_path)
    modulename, _ = os.path.splitext(f_name)

    if path not in sys.path:
        sys.path.insert(0, path)
    return __import__(modulename)


def all_worker_exit_msg(toolbox):
    """
    Warning: Signal stop event to [ALL] -----> WORKER modules, not process.

    :params: toolbox: tools and Queues for processes
    """
    stop_token_lst = [const.RESULT_HEADER_PROC,
                      const.STOP_MSG]  # 'STOP' was sent if last list was produced; now we inform other worker

    for q in toolbox.all_qs_lst_dct:  # next worker on any q reads 'stop_token_lst', except 'mp_print_q'
        if q.empty():
            q.put(stop_token_lst)

    toolbox.mp_output_q.put([toolbox.stop_confirm])  # essential msg for caller, count stop to exit
    toolbox.mp_print_q.put(f'\texit WORKER {toolbox.worker_id}')
    pass


def mp_worker_entry(**kwargs):
    """Entry.
    We are 'disconnected' from parent process now.
    Only Queue communication. Threads can exec() 'string' commands.
    All references are dead. Variables ok. We read only, here.
    """
    worker = None
    # assembled vars and names
    name = mp.process.current_process().name
    proc_id = name.split('-')
    tool_box = {name: ToolBox()}
    tool_box[name].__dict__.update(kwargs)  # ToolBox class, add user defined attributes of ModuleConfiguration inst
    # defaults
    tool_box[name].worker_id = int(proc_id[1])
    tool_box[name].worker_pid = int(os.getpid())
    tool_box[name].worker_name = name
    tool_box[name].stop_msg = const.STOP_MSG
    tool_box[name].stop_confirm = const.STOP_CONFIRM + name
    tool_box[name].result_header_proc = const.RESULT_HEADER_PROC
    tool_box[name].perf_header_eta = const.PERF_HEADER_ETA  # performance list header for ProcInfo
    tool_box[name].perf_current_eta = None
    tool_box[name].kwargs = kwargs

    toolbox = tool_box[name]  # use normal instance like

    # Module Loader
    mod_fun_lst = []
    for row in kwargs['worker_modules']:
        if len(row):
            path_t, ref_t = row.items()
            worker_path, worker_ref = path_t[1], ref_t[1]

            worker_mod = module_path_load(worker_path)  # str path to -> imported module now available
            fun_ref_exec = getattr(worker_mod, worker_ref)  # reference: can make function call now
            mod_fun_lst.append(fun_ref_exec)

    # Function executor
    if len(mod_fun_lst):
        mod_fun_len = len(mod_fun_lst)

        for workmate in range(mod_fun_len):
            if len(mod_fun_lst) >= 2:
                mate_fun = mod_fun_lst.pop()
                mate_fun(toolbox)
        worker = mod_fun_lst.pop()  # last but not least

    while 1:

        busy = worker(toolbox)  # until worker reads the iterator STOP msg
        if not busy:
            if 'stop_msg_disable' not in toolbox.kwargs or not toolbox.kwargs['stop_msg_disable']:
                all_worker_exit_msg(toolbox)  # stop msg in all queues, if not all loaded worker are threads
            break

    while 1:

        msg_lst = toolbox.mp_process_q.get()  # loader keeps proc alive and awaits, 'stop_proc'
        if const.STOP_PROCESS in msg_lst:
            break
