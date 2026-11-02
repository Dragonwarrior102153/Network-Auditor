# Network Auditor

Network Auditor has two user interfaces for inspecting devices and TCP ports
on networks you are authorized to inspect:

- A Python command-line interface (CLI).
- A React frontend that sends requests to a FastAPI backend.

## How the application fits together

### Web application

1. `frontend/Network-Auditor/index.html` contains the root DOM element.
2. `src/main.tsx` mounts the React application into that element.
3. `src/App.tsx` requests a LAN scan and displays a loading screen until the
   request finishes.
4. `src/Api.tsx` sends HTTP requests to the local backend at
   `http://127.0.0.1:8000`.
5. `src/components/NetworkGui.tsx` lays clients out around a router. Selecting
   a client opens `ShowPort.tsx`, which requests and displays its open ports.

The browser only displays data returned by the backend; network discovery and
port checks are performed by Python.

### Backend request flow

`backend/main.py` defines the FastAPI application and routes:

| Route | Purpose | Response |
|---|---|---|
| `GET /` | Confirm the API is reachable. | A short status message. |
| `GET /scanLan` | Scan the interface named `Wi-Fi` and store discovered clients. | Client objects with IP, MAC, name, and type fields. |
| `GET /scanPorts?addr=<ip>` | Scan TCP ports 1–65535 on an address. | A list of open port numbers. |
| `GET /scanSpecificPort?addr=<ip>&port=<number>` | Check one TCP port. | The port number and its state. |
| `GET /showDevices` | Read saved device history. | Saved device records. |

LAN discovery uses active IPv4 interfaces and ARP requests. The web route scans
only an interface named exactly `Wi-Fi` and declines networks with a prefix
shorter than `/16`. Device names are looked up using NetBIOS, reverse DNS, and
mDNS. If a scan finds clients, their MAC addresses are used to insert or update
records in the SQLite database.

Port checks use TCP connection attempts. A timeout is reported internally as
`Indeterminate`; `/scanPorts` returns only ports reported as open. Its full
range scan may take a while, and a timeout does not prove a port is closed.

## Running the project

### Python CLI

Install the backend dependencies in your Python environment:

```powershell
python -m pip install fastapi uvicorn psutil scapy zeroconf pysmb
```

From the repository root, start the CLI:

```powershell
python -m cli.main
```

The menu supports:

- **S**: choose an active IPv4 interface and discover devices on its subnet.
- **O**: scan all TCP ports on an entered address.
- **P**: check one TCP port.
- **Show**: display saved devices.
- **Delete**: drop the device-history table.
- **Exit**: quit the CLI.

For Scapy ARP discovery on Windows, Npcap and an elevated terminal may be
required.

### Build a Windows executable for the React frontend

The web version runs the Python API locally and opens the React interface in
your browser. Build the React files, then package them with the API:

```powershell
cd frontend/Network-Auditor
npm ci
npm run build
cd ../..
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm NetworkAuditor.spec
```

Run `dist\NetworkAuditor.exe` to start the local server and open the frontend.
Keep the console window open while using the app; closing it stops the server.
The executable stores `DevicesTracker.sqlite` beside itself. This is a
Windows-specific build, and Scapy network discovery may still require Npcap
and an elevated terminal.

### React frontend and API

Install frontend dependencies and start the development server:

```powershell
cd frontend/Network-Auditor
npm ci
npm run dev
```

In another terminal, start FastAPI from the backend directory so its local
module imports resolve:

```powershell
cd backend
python -m uvicorn main:app --reload --port 8000
```

The backend permits browser requests from the Vite origins
`http://localhost:5173` and `http://127.0.0.1:5173`.

Build the frontend and run its TypeScript check with:

```powershell
cd frontend/Network-Auditor
npm run build
```

## Database

`DevicesDb` stores records in `DevicesTracker.sqlite` relative to the backend's
current working directory. MAC address is the primary key; each record includes
the most recently seen IP address and first/last-seen timestamps. The database
file is generated at runtime.

## Source code guide

### Python backend

- `backend/main.py`: FastAPI application, CORS configuration, and HTTP routes.
- `backend/discoverDevices.py`: interface discovery, ARP scanning, device-name
  lookups, and recording discoveries.
- `backend/mDNSclass.py`: Zeroconf listener that gathers advertised service
  details and matches them to IP addresses.
- `backend/scanTarget.py`: asynchronous TCP connection checks and full port
  range scanning.
- `backend/devicesDb.py`: SQLite table creation and device record operations.

### Python CLI

- `cli/main.py`: CLI program entry point.
- `cli/cli.py`: interactive menu and calls into discovery, port scanning, and
  device history.

### React frontend

- `frontend/Network-Auditor/index.html`: browser page and React mount element.
- `src/main.tsx`: React DOM entry point.
- `src/App.tsx`: initial LAN scan, loading state, and top-level page.
- `src/Api.tsx`: HTTP helpers for the backend routes.
- `src/components/NetworkGui.tsx`: device types, circular map layout, and
  selection of a client.
- `src/components/ShowPort.tsx`: port-scan request, popup, and loading/error/
  result display.
- `src/components/loading.tsx`: full-page scan indicator.
- `src/App.css`: app-level stylesheet (currently empty).
- `src/components/NetworkGui.css`: network map, connection lines, and device
  card styles.
- `src/components/ShowPort.css`: port popup and its spinner styles.
- `src/components/loading.css`: loading spinner and full-page layout.
- `package.json`: frontend dependencies and the `dev`, `build`, and `preview`
  scripts.
- `tsconfig.json` and `tsconfig.node.json`: TypeScript compiler settings for
  the frontend and Vite configuration.
- `vite.config.ts`: Vite React plugin configuration.
- `src/vite-env.d.ts`: Vite client type declarations for TypeScript.
