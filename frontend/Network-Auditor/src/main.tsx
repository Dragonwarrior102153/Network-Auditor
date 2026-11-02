import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// Mount the React app into the root element from index.html.
ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
