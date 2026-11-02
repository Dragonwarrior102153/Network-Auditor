import { useEffect, useState } from "react";
import { scanOpenPorts } from "../Api";
import "./loading.css";
import "./ShowPort.css";

interface Props {
  addr: string;
  onClose: () => void;
}

/** Show a popup that scans and lists the open TCP ports for one address. */
export default function ShowPort({ addr, onClose }: Props) {
  const [ports, setPorts] = useState<number[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Ignore results after the popup unmounts so a closed popup is not updated.
    let active = true;

    async function loadPorts() {
      try {
        const result = await scanOpenPorts(addr);
        if (active) setPorts(result);
      } catch (error) {
        if (active) {
          setError(error instanceof Error ? error.message : "Port scan failed");
        }
      }
    }

    loadPorts();

    return () => {
      active = false;
    };
  }, [addr]);

  return (
    <div className="port-popup-backdrop" onClick={onClose}>
      <section
        className="port-popup"
        onClick={(event) => event.stopPropagation()}
      >
        <button className="port-popup-close" type="button" onClick={onClose}>
          ×
        </button>
        <h2>Open ports for {addr}</h2>
        {error ? (
          <p>{error}</p>
        ) : ports === null ? (
          <div className="port-popup__loading">
            <div className="loader port-popup-spinner" />
            <p>Scanning ports...</p>
          </div>
        ) : ports.length > 0 ? (
          <p>{ports.join(", ")}</p>
        ) : (
          <p>No open ports found.</p>
        )}
      </section>
    </div>
  );
}
