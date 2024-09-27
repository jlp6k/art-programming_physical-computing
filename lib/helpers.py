from time import ticks_ms, ticks_add, ticks_diff

_call_ids = {}

def call_every(function, *args, id=None, count=None, delay_ms=None, **kwargs):
    """call_every() calls the function passed in parameter with *args and **kwargs.
    But call_every() has three parameters that keep the function to be called.
    The count parameter is an integer which allows the function to be actually called one time over
    the specified number of calls.
    The delay_ms parameter does the same as the count parameter but instead of counting the number of calls,
    it counts time delay between two calls in milliseconds.

    A third keyword parameter called id is used to differentiate the various calls. If not specified,
    the call_every() function works as if function is directly called (i.e. count and delay_ms parameters
    are ignored).

    If both count and delay_ms parameters are specified, the delay_ms is ignored and count is used to
    control the behavior of the function.

    Note: it's probably not a good idea to use count and delay_ms with the same id.
    """
    if id is not None:
        if count is not None:
            # _call_ids[id] is considered as a count
            # By default, it's 0
            if _call_ids.get(id, 0) <= 0:
                # The count of calls as been reached, let's call function
                function(*args, **kwargs)
                # And reset the counter
                _call_ids[id] = count - 1
            else:
                # Decrease the counter
                _call_ids[id] -= 1
            # Exit the function
            return
        elif delay_ms is not None:
            # _call_ids[id] is considered as a delay
            # By default, it's 0
            if ticks_diff(ticks_ms(), _call_ids.get(id, 0)) > 0:
                # The delay between calls is due, let's call function
                function(*args, **kwargs)
                # And reset the time of the next function call
                _call_ids[id] = ticks_add(ticks_ms(), delay_ms)
            # Exit the function
            return
    # Normal function call occurs when:
    # id is None, that's probably because no id has been provided,
    # or
    # both count and delay_ms are None, so no condition applies
    function(*args, **kwargs)

def print_every(*args, id=None, **kwargs):
    """print_every() prints its parameters.
    But print_every() has three parameters that keep the function to print.
    The count parameter is an integer which allows the print to be done one time over
    the specified number of calls.
    The delay_ms parameter does the same as the count parameter but instead of counting the number of calls,
    it counts time delay between two prints in milliseconds.

    A third keyword parameter called id is used to differentiate the various calls. If not specified,
    the print_every() function works as the builtin print() (i.e. count and delay_ms parameters
    are ignored).

    If both count and delay_ms parameters are specified, the delay_ms is ignored and count is used to
    control the behavior of the function.

    Note: it's probably not a good idea to use count and delay_ms with the same id.
    """
    if id is not None:
        id = "print_every_" + str(id)

    call_every(print, *args, id=id, **kwargs)


if __name__ == "__main__":
    from time import sleep

    # The following infinite loop runs twice per second.
    while True:
        print("Loop start")
        # Hello is printed once in 5.
        call_every(print, "Hello", count=5, id=1)
        # World is printed once every 2 seconds.
        print_every("World", delay_ms=2000, id=2)
        sleep(0.5)
        print("Loop end")
