import NetworkGui, { type Client } from "./components/NetworkGui";

const clients: Client[] = [
  {
    name: "Laptop",
    ip: "192.168.1.10",
    mac: "00:00:00:00:00:10",
    type: "laptop",
  },
  {
    name: "Printer",
    ip: "192.168.1.20",
    mac: "00:00:00:00:00:20",
    type: "printer",
  },
  {
    name: "Phone",
    ip: "192.168.1.30",
    mac: "00:00:00:00:00:30",
    type: "phone",
  },
];

function App() {
  return (
    <main>
      <NetworkGui clients={clients} />
    </main>
  );
}

export default App;
