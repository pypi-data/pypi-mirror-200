import requests

from lprp_core.service import Service, optionally_syncronized


class LicensePlateRecognition(Service):

    def __init__(self, address: str):
        self.address = address

    @optionally_syncronized
    async def is_available(self) -> bool:
        response = requests.get(f"{self.address}/is_available")
        return response.json()["is_available"]

    @optionally_syncronized
    async def get_license_plate(self, image: bytes, threshold: int = 128) -> list:
        response = requests.get(f"{self.address}/predict", files={"image": image})
        return response.json()["plates"]
