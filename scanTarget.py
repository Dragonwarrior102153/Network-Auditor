"""TCP port scanning helpers for a single IPv4 target."""

import time
import socket
import errno

class ScanTarget():
    # Check selected TCP ports on a host using connect attempts.

    def __init__(self, targetAddress, timeout) -> None:
        # Set the target (localhost when omitted) and socket timeout.
        self.targetAddress = targetAddress if targetAddress else "127.0.0.1"
        self.ports = [x for x in range(1024)]
        self.timeout = timeout

    def checkOpenPorts(self) -> list[int]:
        # Return open TCP ports in the range 0 through 1023.
        openPorts = []
        for port in self.ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(self.timeout)
                    sock.connect((self.targetAddress, port))
                openPorts.append(port)
            except OSError as err:
                pass

        return openPorts

    def scanPort(self, port) -> list[str | float]:
        # Return the port state and elapsed seconds for one TCP port.
        startTime = time.perf_counter()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect((self.targetAddress, port))
            endTime = time.perf_counter()
            return ["Open", endTime - startTime]
        except OSError as err:
            endTime = time.perf_counter()
            if (err.errno == errno.ECONNREFUSED):
                return ["Closed", endTime - startTime]
            else:
                return ["Indeterminate", endTime - startTime]

                    
