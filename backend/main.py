from fastapi import FastAPI, WebSocket
import numpy as np
import cv2
from mario_env import MarioEnv
from stable_baselines3 import PPO

app = FastAPI()

# Load AI Model
model = PPO.load("models/mario_ai_model.zip")

# Initialize Mario AI Environment (headless mode)
env = MarioEnv(render_mode="rgb_array")
obs, _ = env.reset()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    done = False

    while not done:
        # AI Chooses an Action
        action, _ = model.predict(obs)

        # Apply Action to Environment
        obs, reward, done, _, _ = env.step(action)

        # Capture the game frame
        frame = env.render()
        frame = cv2.resize(frame, (400, 300))  # Resize for faster streaming
        _, buffer = cv2.imencode(".jpg", frame)
        image_bytes = buffer.tobytes()

        # Send Frame to WebSocket
        await websocket.send_bytes(image_bytes)

    env.close()
