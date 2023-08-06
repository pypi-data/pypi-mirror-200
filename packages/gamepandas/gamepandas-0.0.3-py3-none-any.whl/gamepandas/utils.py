from functools import wraps

def stable_type(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        obj = func(self, *args, **kwargs)
        obj.__class__ = self.__class__
        return obj
    return wrapper