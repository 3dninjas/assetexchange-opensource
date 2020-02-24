import Queue as queue
import threading
import c4d

PLUGIN_ID = 1054539  # label: artassetninjac4dmainthread, officially registered id

_main_thread_exec_queue = queue.Queue()


def execute_on_main_thread(original_function):
    def new_function(*args, **kwargs):
        # skip delegation, if we are on main thread alread
        if c4d.threading.GeIsMainThread():
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
        c4d.SpecialEventAdd(PLUGIN_ID)
        # wait for result
        completion_event.wait()
        # raise exception if required
        if queue_item['exception'] is not None:
            raise RuntimeError(queue_item['exception'])
        # return result
        return queue_item['return']
    return new_function


class MainThreadDelegationPlugin(c4d.plugins.MessageData):
    def GetTimer(self):
        return 0

    def CoreMessage(self, id, bc):
        if id == PLUGIN_ID:
            while not _main_thread_exec_queue.empty():
                task = _main_thread_exec_queue.get()
                try:
                    task['return'] = task['function'](
                        *task['args'], **task['kwargs'])
                except Exception as e:
                    task['exception'] = str(e)
                task['completion'].set()
        return True


def register_main_thread_delegate():
    c4d.plugins.RegisterMessagePlugin(
        PLUGIN_ID, "Main Thread Delegation Plugin", 0, MainThreadDelegationPlugin())
