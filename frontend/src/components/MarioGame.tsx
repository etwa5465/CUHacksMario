import React, { useEffect, useRef, useState } from "react";

const MarioGame: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [connected, setConnected] = useState<boolean>(false);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws");

    socket.onopen = () => {
      setConnected(true);
      console.log("✅ Connected to WebSocket");
    };

    socket.onmessage = (event) => {
      const img = new Image();
      img.src = "data:image/jpeg;base64," + btoa(event.data);
      img.onload = () => {
        if (canvasRef.current) {
          const ctx = canvasRef.current.getContext("2d");
          if (ctx) {
            ctx.clearRect(0, 0, 400, 300);
            ctx.drawImage(img, 0, 0, 400, 300);
          }
        }
      };
    };

    socket.onclose = () => {
      setConnected(false);
      console.log("❌ WebSocket Disconnected");
    };

    return () => socket.close();
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <h1>Mario AI</h1>
      <h2>Status: {connected ? "🟢 Connected" : "🔴 Disconnected"}</h2>
      <canvas ref={canvasRef} width="400" height="300" style={{ border: "2px solid black" }} />
    </div>
  );
};

export default MarioGame;
