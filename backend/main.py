from fastapi import FastAPI, WebSocket
import numpy as np
import cv2
import asyncio
from stable_baselines3 import PPO
from mario_env import CustomMarioEnv  

app = FastAPI()

# ✅ Load the AI model
MODEL_PATH = "models/mario_ai_model.zip"
model = PPO.load(MODEL_PATH)
env = CustomMarioEnv()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    obs = env.reset()
    done = False

    try:
        while True:
            action, _ = model.predict(obs)
            obs, reward, done, _ = env.step(action)
            env.render()  

            frame = env.get_frame()  
            _, buffer = cv2.imencode(".jpg", frame)  
            await websocket.send_bytes(buffer.tobytes())

            if done:
                obs = env.reset()

            await asyncio.sleep(0.03)  
    except Exception as e:
        print("WebSocket Error:", e)
    finally:
        env.close()
