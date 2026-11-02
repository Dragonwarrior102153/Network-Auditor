import "./loading.css";

/** Full-screen spinner displayed while the LAN scan is running. */
export default function Loading() {
  return (
    <main className="loadingScreen">
      <div className="loader"></div>
      <p className="loadingText">Scanning Network</p>
    </main>
  );
}
