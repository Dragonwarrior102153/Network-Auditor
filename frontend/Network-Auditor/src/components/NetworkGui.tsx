import { Laptop, Printer, Router, Smartphone } from "lucide-react";
import { useState } from "react";
import ShowPort from "./ShowPort";
import "./NetworkGui.css";

/** Device details supplied by the backend and displayed in the network map. */
export interface Client {
  ip: string;
  mac: string;
  name?: string;
  type?: "laptop" | "printer" | "phone";
}

/** The list of client devices drawn around the router. */
interface Props {
  clients: Client[];
}

/** Draw the network map and open a port scan when a client is selected. */
function NetworkGui({ clients }: Props) {
  const [selectedDevice, setSelectedDevice] = useState<Client | null>(null);

  // Build a display position for every client. The returned array preserves
  // the input order and carries the original client alongside its coordinates,
  // so the same layout can be used by both the SVG connections and the device
  // elements below.
  const devices = clients.map((client, index) => {
    // Distribute clients at equal angular intervals around a full circle.
    // Subtracting π/2 rotates the first position to the top; increasing the
    // index then moves each following position clockwise. The denominator is
    // clamped to at least 1 to avoid division by zero for an empty client list.
    const angle =
      (2 * Math.PI * index) / Math.max(clients.length, 1) - Math.PI / 2;

    // Convert that polar angle to percentage coordinates in the 100 × 100
    // map. The center is (50%, 50%) and the radius is 36 percentage points,
    // leaving room near the edges for device labels and icons.
    return {
      client,
      x: 50 + 36 * Math.cos(angle),
      y: 50 + 36 * Math.sin(angle),
    };
  });

  return (
    <section className="network-map" aria-label="Network devices">
      <svg
        className="network-map__connections"
        viewBox="0 0 100 100"
        aria-hidden="true"
      >
        {devices.map(({ client, x, y }) => (
          <line key={client.mac} x1="50" y1="50" x2={x} y2={y} />
        ))}
      </svg>

      <div className="network-map__device network-map__router">
        <Router aria-hidden="true" />
        <span>Router</span>
      </div>

      {devices.map(({ client, x, y }) => {
        // Use the detected kind when available; unknown devices use the laptop
        // icon as a general-purpose fallback.
        const Icon =
          client.type === "printer"
            ? Printer
            : client.type === "phone"
              ? Smartphone
              : Laptop;

        return (
          <button
            type="button"
            className="network-map__device network-map__client"
            key={client.mac}
            style={{ left: `${x}%`, top: `${y}%` }}
            title={`${client.name ?? client.ip} (${client.ip})`}
            onClick={() => setSelectedDevice(client)}
          >
            <Icon aria-hidden="true" />
            <span>{client.name ?? client.ip}</span>
          </button>
        );
      })}

      {selectedDevice && (
        <ShowPort
          addr={selectedDevice.ip}
          onClose={() => setSelectedDevice(null)}
        />
      )}
    </section>
  );
}

export default NetworkGui;
