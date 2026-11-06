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


<img width="960" height="484" alt="image" src="https://github.com/user-attachments/assets/b0233939-912c-4fcd-b160-e19329ef06c0" />

<img width="489" height="474" alt="image" src="https://github.com/user-attachments/assets/5b943a7c-8dbf-402a-af93-f73f006028bd" />

<img width="613" height="400" alt="image" src="https://github.com/user-attachments/assets/646ca466-f6ab-4bc5-903f-fe5942c84f13" />

<img width="405" height="199" alt="image" src="https://github.com/user-attachments/assets/a1a2eca5-a43b-4ed9-baa6-d90f9d3620a8" />

