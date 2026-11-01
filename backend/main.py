import ipaddress
import asyncio

from devicesDb import DevicesDb
from scanTarget import ScanTarget
from discoverDevices import DiscoverDevices

from fastapi import FastAPI

app = FastAPI()
discoverDevices = DiscoverDevices()


@app.get("/")
def home():
    return {"message": "Network Auditor API is running"}


@app.get("/scanLan")
async def scanLan():
    ifaces = discoverDevices.scanForInterfaces()
    wifiIface = None
    clients = None
    for x in ifaces:
        if (x[0] == "Wi-Fi"):
            wifiIface = x
    if (wifiIface):
        cidr = ipaddress.IPv4Network(f"0.0.0.0/{wifiIface[2]}").prefixlen
        if (cidr >= 16):
            targetAddr = wifiIface[1] + "/" + str(cidr)
            clients = await discoverDevices.findDevices(targetAddr)
            if (clients):
                discoverDevices.trackDevices(clients)
            return clients
        else:
            return "Subnet is too large"


@app.get("/scanPorts")
async def scanPorts(addr):
    return await ScanTarget(addr, 0.5).checkOpenPorts()


@app.get("/scanSpecificPort")
async def scanSpecificPort(addr, port):
    return await ScanTarget(addr, 1).checkPort(port, asyncio.Semaphore(1))


@app.get("/showDevices")
def showDevices():
    vals = DevicesDb().readAll()
    devices = []
    for val in vals:
        devices.append(
            (
                "IP: ", val[1],
                "MAC: ", val[0],
                "first seen: ", val[2],
                "last seen:", val[3],
            )
        )

    return devices
