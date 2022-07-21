from IPython.display import display


def display_return(wrapped_function, **initial_kwargs):
    def _display_return(*args, **kwargs):
        display(wrapped_function(*args, **initial_kwargs, **kwargs))

    return _display_return
