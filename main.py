from scanTarget import ScanTarget

def main():
    testRun = ScanTarget(None, .25)
    print(testRun.checkOpenPorts())

if (__name__ == "__main__"):
    main()