import time
import socket
import errno

class ScanTarget:
    def __init__(self, targetAddress, timeout) -> None:
        self.targetAddress = targetAddress if targetAddress else "127.0.0.1"
        self.ports = [22, 23, 25, 53, 80, 139, 443]
        self.timeout = timeout

    def checkOpenPorts(self) -> list[int]:
        openPorts = []
        try:
            for port in self.ports:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(self.timeout)
                        sock.connect((self.targetAddress, port))
                    openPorts.append(port)
                except OSError as err:
                    print(str(err))                    
        except:
            print("Error encountered")

        return openPorts

    def scanPort(self, port) -> list[str | float]:
        startTime = time.perf_counter()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(.25)
                sock.connect((self.targetAddress, port))
            endTime = time.perf_counter()
            return ["Open", endTime - startTime]
        except OSError as err:
            endTime = time.perf_counter()
            if (err.errno == errno.ECONNREFUSED):
                return ["Closed", endTime - startTime]
            else:
                return ["Indeterminate", endTime - startTime]

                    

