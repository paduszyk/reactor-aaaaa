import functools

__all__ = ["on_ready"]


def on_ready(**kwargs):
    """Return a decorator wrapping a method of an app config class such that that method
    is marked as one that should be automatically called by the config's `ready()` hook.
    """

    def decorator(method):
        @functools.wraps(method)
        def wrapper(self):
            return method(self)

        # Mark the wrapper by the decorator name.
        setattr(wrapper, on_ready.__name__, True)

        return wrapper

    return decorator
