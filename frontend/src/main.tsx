import React from "react";
import ReactDOM from "react-dom/client";
import MarioGame from "./components/MarioGame"; // Ensure this file exists
import "./style.css"; // Keep existing styles

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <MarioGame />
  </React.StrictMode>
);
