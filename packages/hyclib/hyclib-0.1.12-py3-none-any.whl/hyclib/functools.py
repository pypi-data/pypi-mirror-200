import functools
import warnings

from . import pprint

def parametrized(dec):
    """
    A decorator for decorators.
    Copied from @Dacav's answer here: https://stackoverflow.com/questions/5929107/decorators-with-parameters
    """
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

@parametrized
def deprecated(func, msg=""):
    """This is a decorator which can be used to mark functions
    as deprecated."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn(f"Call to deprecated function {func.__name__}. {msg}",
                      category=DeprecationWarning,
                      stacklevel=2)
        return func(*args, **kwargs)
    return new_func
