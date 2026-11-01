"""TCP port scanning helpers for a single IPv4 target."""

import time
import socket
import errno
import asyncio


class ScanTarget:
    # Check selected TCP ports on a host using connect attempts.

    def __init__(self, targetAddress, timeout) -> None:
        # Set the target (localhost when omitted) and socket timeout.
        self.targetAddress = targetAddress if targetAddress else "127.0.0.1"
        self.timeout = timeout

    async def checkOpenPorts(self) -> list[int]:
        # Return open TCP ports.
        openPorts = []
        semaphore = asyncio.Semaphore(200)
        for window in range(1, 65536, 200):
            cap = 200 if (window + 200 <= 65536) else 65536 - window
            tasks = [
                asyncio.create_task(self.checkPort(port, semaphore))
                for port in range(window, window + cap)
            ]
            results = await asyncio.gather(*tasks)

            if (results):
                for result in results:
                    if (result and result[1] == "Open"):
                        openPorts.append(result[0])

        return openPorts

    async def checkPort(self, port, semaphore) -> tuple[int, str]:
        try:
            async with semaphore:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(self.targetAddress, port),
                    timeout=self.timeout,
                )
                writer.close()
                await writer.wait_closed()

            return (port, "Open")

        except asyncio.TimeoutError:
            return (port, "Indeterminate")

        except OSError as err:
            if (err.errno == errno.ECONNREFUSED):
                return (port, "Closed")
            else:
                return (port, "Indeterminate")


"""
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
            

"""
