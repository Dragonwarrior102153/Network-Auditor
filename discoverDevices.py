import socket
import psutil

class DiscoverDevices():
    def __init__(self) -> None:
        pass

    def scanForInterfaces(self) -> list[tuple[str, str]]:
        interfaces = []
        netStatsRaw = psutil.net_if_stats()
        netStatsAddress = psutil.net_if_addrs()

        for iface, info in netStatsRaw.items():
            if (iface not in netStatsAddress):
                continue

            for addr in netStatsAddress[iface]:
                if (addr.family == socket.AF_INET and info.isup):
                    interfaces.append((iface, addr.address))


        return interfaces
