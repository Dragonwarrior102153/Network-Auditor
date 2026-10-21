from scanTarget import ScanTarget
from discoverDevices import DiscoverDevices

def main():
    testRun = ScanTarget(None, 1)
    print(testRun.scanPort(4321))

    testDevices = DiscoverDevices()
    print(testDevices.scanForInterfaces())


if (__name__ == "__main__"):
    main()