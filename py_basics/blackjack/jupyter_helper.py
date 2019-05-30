"""
Helper functions for use with jupyter notebooks
"""


# Imports
from IPython.display import clear_output



def clear_display():
    """
    Clear the output below current cell. This is useful for when wanting to overwrite output in a loop

    Returns
    -------
    None
    """
    if is_notebook():
        clear_output(wait=True)


def is_notebook():
    """
    Return whether the current code is being executed in a jupyter notebook or not

    Returns
    -------
    output : bool
        True if code being executed is in a jupyter notebook, otherwise False
    """
    
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter
