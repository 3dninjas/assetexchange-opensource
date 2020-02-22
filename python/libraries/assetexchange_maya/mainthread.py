import maya.utils

def execute_on_main_thread(original_function):
    def new_function(*args, **kwargs):
        # delegate to main thread
        return maya.utils.executeInMainThreadWithResult( original_function, *args, **kwargs)
    return new_function
