"""Launch the web application and open its local frontend in a browser."""

import os
from pathlib import Path
import socket
import sys
import threading
import time
import webbrowser


if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(APP_DIR / "backend"))

os.chdir(APP_DIR)

import main as backend
import uvicorn


def main() -> None:
    """Run the local API until the user closes this process."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        listening_socket.bind(("127.0.0.1", 0))
        listening_socket.listen(2048)
        listening_socket.setblocking(False)
        port = listening_socket.getsockname()[1]
        server = uvicorn.Server(
            uvicorn.Config(backend.app, host="127.0.0.1", port=port)
        )
        server_thread = threading.Thread(
            target=server.run,
            kwargs={"sockets": [listening_socket]},
            daemon=True,
        )
        server_thread.start()

        deadline = time.monotonic() + 30
        while not server.started and server_thread.is_alive():
            if time.monotonic() >= deadline:
                server.should_exit = True
                server_thread.join()
                raise RuntimeError(
                    "The web server did not start within 30 seconds."
                )
            time.sleep(0.1)

        if not server.started:
            raise RuntimeError("The web server stopped before it finished starting.")

        url = f"http://127.0.0.1:{port}/"
        print(
            f"Network Auditor is running at {url}. Press Ctrl+C to stop.",
            flush=True,
        )
        webbrowser.open(url)

        try:
            server_thread.join()
        except KeyboardInterrupt:
            server.should_exit = True
            server_thread.join()


if __name__ == "__main__":
    main()
