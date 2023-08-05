from lprp_core.service import Service, optionally_syncronized


class UserInterfaceBackend(Service):
    def __init__(self, address: str):
        pass

    @optionally_syncronized
    async def is_available(self) -> bool:
        raise NotImplementedError
