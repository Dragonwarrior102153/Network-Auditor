import NetworkGui, { type Client } from "./components/NetworkGui";
import { scanLan } from "./Api";
import Loading from "./components/loading";
import { useState, useEffect } from "react";

/** Load the LAN scan once and show either its loading screen or network map. */
function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [clients, setClients] = useState<Client[]>([]);

  useEffect(() => {
    // Fetching is asynchronous, so keep the loading screen visible until it
    // succeeds or fails; the finally block always ends the loading state.
    async function loadNetwork() {
      try {
        const results = await scanLan();
        setClients(results);
      } catch (error) {
        console.error("Network scan failed:", error);
      } finally {
        setIsLoading(false);
      }
    }

    loadNetwork();
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <main>
      <NetworkGui clients={clients} />
    </main>
  );
}

export default App;
