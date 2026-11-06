# Network Auditor

## What it is

A Windows desktop app that discovers devices on your local network and checks
their TCP ports.

## Motivation

I have been studying networking concepts for fbla events last year, but I have not done anything hands on yet, so I made a project that combines my coding and networking experiences, while making it easy to audit a network.

## Requirements

- Windows and an active Wi-Fi or Ethernet connection.
- [Npcap](https://npcap.com/#download) for local-network discovery. Enable
  **WinPcap API-compatible Mode** if offered.
- No separate Python or Node.js installation is needed; the executable bundles
  the app and its dependencies.

## How to play

1. Install Npcap on the computer running the app.
2. Run `NetworkAuditor.exe` from a writable folder. It opens in your browser;
   keep the console window open.
3. Wait for local devices to appear, then select a device to scan its TCP
   ports. A full port scan can take several minutes.

Use only on networks and devices you are authorized to inspect.
