import os
import shelve
from functools import wraps
from inspect import signature


def snap(output_dir='/tmp'):
    """Save the input(s) and output(s) of
    the wrapped function"""
    def decorator(fn):
        fname = '{}.{}'.format(fn.__module__, fn.__name__)
        path = os.path.join(output_dir, fname)
        sig = signature(fn)
        params = list(sig.parameters)

        @wraps(fn)
        def decorated(*args, **kwargs):
            shelf = shelve.open(path, 'c')
            shelf['_args'] = params
            for param, arg in zip(params, args):
                shelf[param] = arg

            shelf['_kwargs'] = list(kwargs.keys())
            for param, arg in kwargs.items():
                shelf[param] = arg

            result = fn(*args, **kwargs)
            shelf['_result'] = result
            shelf.close()
            return result
        return decorated
    return decorator


def test(input_dir, fn_path):
    """Load the input(s) and output(s) of
    the specified dump file and check that
    this function returns the same output(s)"""
    def decorator(fn):
        @wraps(fn)
        def decorated():
            input_path = os.path.join(input_dir, fn_path)
            with shelve.open(input_path, 'r') as shelf:
                args = [shelf[k] for k in shelf['_args']]
                kwargs = {k: shelf[k] for k in shelf['_kwargs']}
                expected = shelf['_result']

            result = fn(*args, **kwargs)
            assert expected == result
            return result
        return decorated
    return decorator