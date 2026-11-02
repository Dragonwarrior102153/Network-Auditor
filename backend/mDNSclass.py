"""Collect service information announced through multicast DNS."""

from zeroconf import ServiceListener
import socket
import asyncio

class MDNSListener(ServiceListener):
    """Store discovered mDNS service details and look them up by IP address."""

    def __init__(self, zc) -> None:
        """Create a listener that uses the provided Zeroconf client."""
        super().__init__()        
        self.info = []
        self.zc = zc

    def add_service(self, zc, type_, name) -> None:
        """Fetch and save details when a service is announced."""
        asyncio.create_task(self.getInfo(type_, name))

    async def getInfo(self, type, name):
        """Retrieve a service's details and append them when available."""
        info = await self.zc.async_get_service_info(type, name)
        if (info):
            self.info.append(info)

    def checkForIp(self, ip) -> str | None:
        """Return the host name of a saved service that advertises this IP."""
        for device in self.info:
            if (ip in device.parsed_addresses()):
                return device.server
            
        return None

    def update_service(self, zc, type_, name) -> None:
        """Handle service updates; this listener does not refresh saved data."""
        pass

    def remove_service(self, zc, type_, name) -> None:
        """Handle service removals; saved entries are kept for this scan."""
        pass