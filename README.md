# Network Auditor

An interactive Python command-line tool for discovering devices on a local
IPv4 subnet, tracking their IP/MAC addresses over time, and checking TCP ports.
Only scan networks and hosts you are authorized to inspect.

## Setup

Install Python 3 and the required packages:

```powershell
python -m pip install psutil scapy
```

On Windows, Scapy's ARP discovery may also require Npcap and an elevated
terminal. Download Npcap at https://npcap.com/#download. Run the app from this directory so its SQLite database is created
here:

```powershell
python main.py
```

## Commands

- **S**: choose an active IPv4 interface and discover devices on its subnet.
  Subnets with a prefix length of less than `/18` are declined as too
  large; only subnets of `/18` or more specific than `/18` can be scanned.
- **O**: check TCP ports 0-1023 on an entered IPv4 host.
- **P**: check one TCP port on an entered IPv4 host.
- **Show**: display devices previously discovered.
- **Exit**: quit the application.

For the port-scanning prompts, enter `none` to use this computer
(`127.0.0.1`). The broad port scan uses a short connection timeout; a
non-response does not necessarily mean a port is closed.

## Device history

`DevicesDb` stores records in `DevicesTracker.sqlite` in the current working
directory. A MAC address identifies each record; scans update its most recent
IP address and last-seen time. The database is generated at runtime and is
excluded from version control.

## Source files

- `main.py` starts the application.
- `cli.py` implements the interactive menu and connects user choices to scans.
- `discoverDevices.py` lists interfaces, discovers ARP responders, and tracks
  discovered devices.
- `scanTarget.py` checks TCP ports on a selected host.
- `devicesDb.py` creates and accesses the SQLite device-history table.
