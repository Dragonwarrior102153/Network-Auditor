import { Laptop, Printer, Router, Smartphone } from "lucide-react";
import "./NetworkGui.css";

export interface Client {
  ip: string;
  mac: string;
  name: string;
  type?: "laptop" | "printer" | "phone";
}

interface Props {
  clients: Client[];
}

function NetworkGui({ clients }: Props) {
  const devices = clients.map((client, index) => {
    const angle =
      (2 * Math.PI * index) / Math.max(clients.length, 1) - Math.PI / 2;
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
        const Icon =
          client.type === "printer"
            ? Printer
            : client.type === "phone"
              ? Smartphone
              : Laptop;

        return (
          <div
            className="network-map__device network-map__client"
            key={client.mac}
            style={{ left: `${x}%`, top: `${y}%` }}
            title={`${client.name} (${client.ip})`}
          >
            <Icon aria-hidden="true" />
            <span>{client.name}</span>
          </div>
        );
      })}
    </section>
  );
}

export default NetworkGui;
