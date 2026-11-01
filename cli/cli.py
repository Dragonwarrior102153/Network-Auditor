
"""Interactive command-line interface for network scanning and device history."""

from backend.discoverDevices import DiscoverDevices
from backend.scanTarget import ScanTarget
from backend.devicesDb import DevicesDb
import ipaddress
import asyncio


class CLI():
    # Prompt for scans and display devices stored in the local database.

    def __init__(self):
        # Initialize scanner services and run the command loop.
        self.loop = True
        self.devicesDb = DevicesDb()
        self.discoverDevices = DiscoverDevices()
        while(self.loop):
            act = self.defaultPrompt().lower()
            if (act == "s"):
                print(asyncio.run(self.scanLAN()))
            elif(act == "o"):
                print(asyncio.run(self.scanForOpenPort()))
            elif(act == "p"):
                print(self.scanPort())
            elif(act == "show"):
                print(self.showDevices())
            elif(act == "delete"):
                self.deleteDb()
            elif(act == "exit"):
                self.exit()


    def defaultPrompt(self):
        # Display available actions and return the user's selection.
        print("\n\nHere is the list of available actions: \nO: scan a device for open ports\nShow: deivces that have been found in the network")
        x = input ("S: scan your LAN for devices on your subnet\nP: Scan a specific port\nExit: quit the app\n")
        return x

    def deleteDb(self):
        self.devicesDb.deleteAll()

    async def scanLAN(self):
        # Select an active interface, scan its subnet, and track responders.
        ifaces = self.discoverDevices.scanForInterfaces()
        i = 0
        for x in ifaces:
            i+=1
            print(i, ": ", x)
        act = int(input("Here are the available interfaces, which interface would you like to scan? (enter the associated number)\n"))
        cidr = ipaddress.IPv4Network(f"0.0.0.0/{ifaces[act-1][2]}").prefixlen
        if (cidr >= 16):
            targetAddr = ifaces[act-1][1] + "/" + str(cidr)
            clients = await self.discoverDevices.findDevices(targetAddr)
            return (clients)
        else:
            return ("Subnet is too large")
        
        
    async def scanForOpenPort(self):
        # Scan TCP ports 0-1023 on the entered host (or localhost).
        act = input("Which ip address would you like to scan? (put none for this device)\n")
        targ = None if act == "none" else act
        scanTarg = ScanTarget(targ, .5)

        return await scanTarg.checkOpenPorts()

    def scanPort(self):
        # Check one TCP port on the entered host (or localhost).
        act = input("Which ip address would you like to scan? (put none to scan this device)\n")
        targ = None if act == "none" else act
        port = int(input("Which port would you like to scan?\n"))
        scanTarg = ScanTarget(targ, .5)

        return scanTarg.scanPort(port)

    def showDevices(self):
        # Return stored devices with their IP, MAC, and first/last-seen times.
        vals = self.devicesDb.readAll()
        devices = []
        for val in vals:
            devices.append(("IP: ", val[1], "MAC: ", val[0], "first seen: ", val[2], "last seen:", val[3]))

        return devices

    def exit(self):
        # Stop the interactive command loop.
        self.loop = False