from functools import wraps


def iterable(func):
    @wraps(func)
    def wrapper(self, arg):
        if isinstance(arg, int):
            return func(self, arg)

        if isinstance(arg, float):
            return func(self, arg)

        if isinstance(arg, list):
            return [func(self, x) for x in arg]

        if isinstance(arg, tuple):
            return (func(self, x) for x in arg)

        raise TypeError("Unsupported data type")

    return wrapper
