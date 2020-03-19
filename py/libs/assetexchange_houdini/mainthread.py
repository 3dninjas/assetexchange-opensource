import hdefereval

def execute_on_main_thread(original_function):
    def new_function(*args, **kwargs):
        # delegate to main thread
        print "Starting on main thread"
        return hdefereval.executeInMainThreadWithResult( original_function, *args, **kwargs)
    return new_function
