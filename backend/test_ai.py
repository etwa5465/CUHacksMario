import torch
import numpy as np
import cv2
from stable_baselines3 import PPO
from mario_env import CustomMarioEnv  # Import your custom environment

# Load environment
env = CustomMarioEnv()

# Load trained model
MODEL_PATH = "models/mario_ai_model.zip"

try:
    model = PPO.load(MODEL_PATH)
    print(f"Loaded model from {MODEL_PATH}")
except FileNotFoundError:
    print(f"Error: Model file {MODEL_PATH} not found! Train the model first.")
    exit()

# Run AI in environment
obs = env.reset()
done = False

while True:  # Infinite loop to keep playing
    action, _ = model.predict(obs)  # AI decides action
    obs, reward, terminated, _, _ = env.step(action)  # Step in env
    
    env.render()  # Show the game window

    if terminated:
        print("Episode finished, restarting...")
        obs = env.reset()
