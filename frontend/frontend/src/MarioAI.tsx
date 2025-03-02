import React, { useEffect, useState, useRef } from "react";

const MarioAI = () => {
  const [status, setStatus] = useState("🔴 Disconnected");
  const [imageSrc, setImageSrc] = useState("");
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    try {
      ws.current = new WebSocket("ws://localhost:8000/ws"); // Connect to WebSocket

      ws.current.onopen = () => {
        setStatus("�� Connected");
      };

      ws.current.onmessage = (event) => {
        const blob = event.data;
        const reader = new FileReader();

        reader.onload = () => {
          if (reader.result) {
            setImageSrc(reader.result as string);
          } else {
            console.warn("WebSocket received an empty message.");
          }
        };

        reader.readAsDataURL(blob);
      };

      ws.current.onerror = (error) => {
        console.error("WebSocket Error:", error);
        setStatus("🔴 Error");
      };

      ws.current.onclose = () => {
        setStatus("🔴 Disconnected");
      };

      return () => {
        ws.current?.close();
      };
    } catch (error) {
      console.error("Failed to connect WebSocket:", error);
      setStatus("🔴 Error");
    }
  }, []);

  return (
    <div style={{ textAlign: "center", color: "white" }}>
      <h1>Mario AI</h1>
      <p>Status: {status}</p>
      {imageSrc && <img src={imageSrc} alt="Mario AI Gameplay" width="512" height="512" />}
    </div>
  );
};

export default MarioAI;

