import time
from functools import wraps


def wait_if_syncing(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        backoff = 1
        max_backoff = 15

        while self._is_syncing:
            print(
                f"\n\n============= Waiting for {backoff} seconds to sync... =============\n\n")
            time.sleep(backoff)
            backoff *= 2
            if backoff > max_backoff:
                backoff = max_backoff

        return func(self, *args, **kwargs)

    return wrapper


def skip_if_syncing(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._is_syncing:
            print(
                f"Skipping {func.__name__} as the node is currently syncing.")
            return

        return func(self, *args, **kwargs)

    return wrapper
