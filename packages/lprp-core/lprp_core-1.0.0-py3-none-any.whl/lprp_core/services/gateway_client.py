from lprp_core.service import Service, optionally_syncronized


class GatewayClient(Service):
    def __init__(self, address: str):
        pass

    @optionally_syncronized
    async def is_available(self) -> bool:
        raise NotImplementedError
