from zeroconf import ServiceListener
import socket
import asyncio

class MDNSListener(ServiceListener):

    def __init__(self, zc) -> None:
        super().__init__()        
        self.info = []
        self.zc = zc

    def add_service(self, zc, type_, name) -> None:
        asyncio.create_task(self.getInfo(type_, name))

    async def getInfo(self, type, name):
        info = await self.zc.async_get_service_info(type, name)
        if (info):
            self.info.append(info)

    def checkForIp(self, ip) -> str | None:
        for device in self.info:
            if (ip in device.parsed_addresses()):
                return device.server
            
        return None

    def update_service(self, zc, type_, name) -> None:
        pass

    def remove_service(self, zc, type_, name) -> None:
        pass