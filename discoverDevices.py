"""Discover IPv4 hosts on local networks and keep their sightings in the database."""

import socket
import psutil
import time
import asyncio
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from devicesDb import DevicesDb
from nmb.NetBIOS import NetBIOS
from mDNSclass import MDNSListener

class DiscoverDevices():
    # Find active IPv4 interfaces and track devices found by ARP scans.

    def __init__(self) -> None:
        # Create the device database used to store discovered hosts.
        self.devicesDb = DevicesDb()

    def scanForInterfaces(self) -> list[tuple[str, str, str]]:
        # Return active IPv4 interfaces as (name, address, netmask) tuples.
        interfaces = []
        netStatsRaw = psutil.net_if_stats()
        netStatsAddress = psutil.net_if_addrs()

        for iface, info in netStatsRaw.items():
            if (iface not in netStatsAddress):
                continue

            for addr in netStatsAddress[iface]:
                if (addr.family == socket.AF_INET and info.isup):
                    interfaces.append((iface, addr.address, addr.netmask))

        print()

        return interfaces

    def calculateAvailableRange(self, addr, netMask) -> str:
        # Return the usable host range for an IPv4 address and dotted netmask.
        netMask = netMask.split(".")
        maskBinSplit = []
        for part in netMask:
            maskBinSplit.append(format(int(part), '08b'))

        addr = addr.split(".")
        addrBinSplit = []
        for part2 in addr:
            addrBinSplit.append(format(int(part2), '08b'))

        firstAddr = ""
        i = 0
        for i in range(4):
            if (maskBinSplit[i] == "00000000"):
                firstAddr += "00000000."
            else:
                for x in range(8):
                    if (maskBinSplit[i][x] == "0"):
                        firstAddr += "0"
                    else:
                        firstAddr += addrBinSplit[i][x]
                firstAddr += "."

        firstAddrInt = [int(byte, 2) for byte in firstAddr.split(".")[:-1]]

        lastAddr = ""
        i = 0
        for i in range(4):
            if (maskBinSplit[i] == "00000000"):
                lastAddr += "11111111."
            else:
                for x in range(8):
                    if (maskBinSplit[i][x] == "0"):
                        lastAddr += "1"
                    else:
                        lastAddr += addrBinSplit[i][x]
                lastAddr += "."

        lastAddrInt = [int(byte2, 2) for byte2 in lastAddr.split(".")[:-1]]

        broadCastAddr = ".".join(map(str, firstAddrInt))
        networkAddr = ".".join(map(str, lastAddrInt))
 
        firstAvailAddr = firstAddrInt.copy()
        firstAvailAddr[3] += 1
        firstAvailAddrStr = ".".join(map(str, firstAvailAddr))

        lastAvailAddr = lastAddrInt.copy()
        lastAvailAddr[3] -= 1
        lastAvailAddrStr = ".".join(map(str, lastAvailAddr))

            
        return (firstAvailAddrStr + " - " + lastAvailAddrStr)

    def findDevices(self, target) -> list[dict[str, str]]:
        # Broadcast an ARP request for target and return responding IP/MAC pairs.
        arp = ARP(pdst=target)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp

        result = srp(packet, timeout=3)[0]

        clients = []

        for sent, received in result:
            clients.append({'ip': received.psrc, 'mac': received.hwsrc})
        
        return clients

    def trackDevices(self, clients):
        # Insert new MAC addresses or update known device sightings.
        values = self.devicesDb.readAll()
        knownDevices = {
            row[0]: row[1]
            for row in values
        }

        for client in clients:
            ip = client['ip']
            mac = client['mac']
            if (not mac in knownDevices):
                self.devicesDb.create(mac, ip, time.time(), time.time())
                knownDevices[mac] = ip
            else:
                self.devicesDb.update(ip, time.time(), mac)
                knownDevices[mac] = ip

    def reverseDNS(self, ip):
        try:
            return socket.gethostbyaddr(ip)
        except (socket.herror, socket.gaierror, OSError):
            return None

    def manualName(self) -> str:
        name = input("What should the device be called?")
        return name 


    #make these an async function so it returns whichever one completes the fastest (if any do); if not, make the user enter manual name (or skip and use ip)
    def mDNS(self):
        pass

    def netBIOSlookup(self, ip):
        nb = NetBIOS()
        try: 
            names = nb.queryIPForName(ip)
            if (names):
                return names[0]
            else:
                return None
        finally:
            nb.close()


    
 

        



