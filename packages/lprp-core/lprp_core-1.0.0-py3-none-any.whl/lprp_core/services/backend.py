from lprp_core.service import Service, optionally_syncronized


class Backend(Service):
    def __init__(self, address: str):
        super().__init__(address=address)

    @optionally_syncronized
    async def is_available(self) -> bool:
        raise NotImplementedError

    @optionally_syncronized
    async def has_permission(self) -> bool:
        raise NotImplementedError
