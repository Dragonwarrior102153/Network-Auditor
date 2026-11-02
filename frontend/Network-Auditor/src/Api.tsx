/** Fetch the discovered clients from the local FastAPI service. */
export async function scanLan() {
  const response = await fetch("/scanLan");

  if (!response.ok) {
    const body: { detail?: string } = await response.json();
    throw new Error(body.detail ?? "Failed to scan the LAN");
  }

  const clients: unknown = await response.json();
  if (
    !Array.isArray(clients) ||
    !clients.every(
      (client) =>
        client &&
        typeof client.ip === "string" &&
        typeof client.mac === "string",
    )
  ) {
    throw new Error("The scan returned an invalid device list.");
  }
  return clients;
}

/** Fetch the open TCP ports found on one device. */
export async function scanOpenPorts(device: string) {
  const response = await fetch(`/scanPorts?addr=${device}`);

  if (!response.ok) {
    throw new Error("Failed to scan device");
  }
  return await response.json();
}

/** Ask the API to check one TCP port on a device. */
export async function scanPort(device: string, port: number) {
  const response = await fetch(
    `/scanSpecificPort?addr=${encodeURIComponent(device)}&port=${port}`,
  );

  if (!response.ok) {
    throw new Error("Failed to scan port");
  }
  return await response.json();
}

/** Fetch the device history saved by the backend. */
export async function showHistory() {
  const response = await fetch("/showDevices");

  if (!response.ok) {
    throw new Error("Failed to retrieve data");
  }
  return response.json();
}
