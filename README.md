# Network Auditor

Network Auditor is a Windows desktop application distributed as
`NetworkAuditor.exe`. The executable includes the React web interface and the
Python API backend that serves it locally. You do not need to install Python,
Node.js, or the project source to run a released executable.

Use the scanner only on networks and devices you own or are authorized to
inspect.

## Requirements to run the executable

- Windows.
- Npcap, required for local-network device discovery with Scapy. Download it
  from the [official Npcap download page](https://npcap.com/#download). Enable
  **WinPcap API-compatible Mode** during installation if the installer offers
  that option.
- A default web browser, which the app opens automatically.
- An active IPv4 network interface named `Wi-Fi`, preferred for the LAN scan.
  If no active `Wi-Fi` interface is found, the app uses an active interface
  named `Ethernet` or `Ethernet` followed by a number (such as `Ethernet 2`).
  It refuses to scan subnets larger than `/16`.
- A writable folder for `NetworkAuditor.exe`. The app creates
  `DevicesTracker.sqlite` beside the executable to save discovered-device
  history.

The executable bundles the Python runtime and backend dependencies, plus the
built React frontend. Python, Node.js, npm, and separate frontend/backend
installations are not needed to run it. Npcap is a Windows system dependency
and is not bundled.

## Run the application

1. Install Npcap using the link above.
2. Place `NetworkAuditor.exe` in a folder where you have write permission.
3. Double-click `NetworkAuditor.exe`. It starts the local backend and opens
   the frontend in your default browser.
4. Keep the console window open while using the app. Close it with **Ctrl+C**
   to stop the backend and application.

If LAN discovery fails, confirm that Npcap is installed and that you are
connected through an active `Wi-Fi` or `Ethernet` interface. Wi-Fi is used
when both are available; Ethernet is the fallback. If needed, try running the
executable as an administrator so packet capture has the required access.

The frontend displays devices that respond to an ARP scan. Selecting a device
allows you to check its TCP ports; a full scan checks ports 1–65535 and may
take a while. A timeout does not mean that a port is closed.

## Build from source

These are build-time requirements only; end users of the executable do not
need them:

- Python 3.10 or later.
- Node.js `^20.19.0` or `>=22.12.0` and npm, as required by the Vite version
  in the frontend lockfile.
- Python packages listed in the root `requirements.txt`.
- Frontend packages, declared in `frontend/Network-Auditor/package.json` and
  locked in `package-lock.json`:
  - App dependencies: `bootstrap`, `lucide-react`, `react`, `react-dom`.
  - Build dependencies: `@types/react`, `@types/react-dom`,
    `@vitejs/plugin-react`, `typescript`, `vite`.

Run `npm ci` to install the locked frontend dependencies and their transitive
dependencies.

From the project directory, build the React assets, install the Python
packages from `requirements.txt`, and run PyInstaller:

```powershell
cd frontend\Network-Auditor
npm ci
npm run build
cd ..\..
python -m pip install -r requirements.txt
pyinstaller --clean --noconfirm NetworkAuditor.spec
```

PyInstaller writes the executable to `dist\NetworkAuditor.exe`. Build the
executable on Windows for Windows; the spec packages the built frontend into
the executable.

## Application details

- `run_web.py` starts the local FastAPI server on `127.0.0.1` using an
  available port, then opens the app in the browser.
- `backend/` implements ARP-based LAN discovery, device-name lookups, TCP port
  checks, and SQLite device history.
- `frontend/Network-Auditor/` contains the React application and Vite build
  configuration.
- `NetworkAuditor.spec` packages the Python application and built frontend
  with PyInstaller.
- `DevicesTracker.sqlite` is created at runtime beside the executable and
  stores discovered devices' MAC addresses, most recently seen IP addresses,
  and first/last-seen times.
