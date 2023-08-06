import asyncio
from abc import ABC, abstractmethod


def optionally_syncronized(f):
    """Decorator to make a function to run a async function synchronously if "sync=True" is passed."""
    def wrapper(*args, sync=False, **kwargs):
        if sync:
            return asyncio.run(f(*args, **kwargs))
        else:
            return f(*args, **kwargs)
    return wrapper


class Service(ABC):
    @abstractmethod
    def __init__(self, address: str):
        self.address = address

    @optionally_syncronized
    @abstractmethod
    async def is_available(self) -> bool:
        pass
