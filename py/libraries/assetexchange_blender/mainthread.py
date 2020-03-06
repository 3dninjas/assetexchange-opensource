import queue
import threading

_main_thread_exec_queue = queue.Queue()


def main_thread_handler():
    had_work = not _main_thread_exec_queue.empty()
    while not _main_thread_exec_queue.empty():
        task = _main_thread_exec_queue.get()
        try:
            task['return'] = task['function'](*task['args'], **task['kwargs'])
        except Exception as e:
            task['exception'] = str(e)
        task['completion'].set()
    if had_work:
        return 0.1
    return 0.2


def execute_on_main_thread(original_function):
    def new_function(*args, **kwargs):
        # skip delegation, if we are on main thread alread
        if threading.current_thread() is threading.main_thread():
            return original_function(*args, **kwargs)
        completion_event = threading.Event()
        queue_item = {
            'function': original_function,
            'args': args,
            'kwargs': kwargs,
            'return': None,
            'exception': None,
            'completion': completion_event
        }
        _main_thread_exec_queue.put(queue_item)
        # wait for result
        completion_event.wait()
        # raise exception if required
        if queue_item['exception'] is not None:
            raise RuntimeError(queue_item['exception'])
        # return result
        return queue_item['return']
    return new_function
