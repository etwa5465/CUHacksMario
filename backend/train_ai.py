import os
import torch
from stable_baselines3 import PPO
from mario_env import CustomMarioEnv  # Import your custom environment

# Ensure models directory exists
if not os.path.exists("models"):
    os.makedirs("models")

# Create custom environment
env = CustomMarioEnv()

# Check if CUDA is available for faster training
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Model path
MODEL_PATH = "models/mario_ai_model.zip"

# Load existing model if available, otherwise create a new one
if os.path.exists(MODEL_PATH):
    print(f"Loading existing model from {MODEL_PATH}")
    model = PPO.load(MODEL_PATH, env=env, device=device)
else:
    print("No existing model found. Creating a new PPO model...")
    model = PPO("CnnPolicy", env, verbose=1, device=device)

# Train AI
TOTAL_TIMESTEPS = 100_000  # Increase for better performance
CHECKPOINT_INTERVAL = 10_000  # Save model every 100k steps

for i in range(TOTAL_TIMESTEPS // CHECKPOINT_INTERVAL):
    print(f"Training iteration {i+1}/{TOTAL_TIMESTEPS // CHECKPOINT_INTERVAL}...")
    model.learn(total_timesteps=CHECKPOINT_INTERVAL, progress_bar=True)
    
    # Save checkpoint
    checkpoint_path = f"models/mario_ai_model_{(i+1) * CHECKPOINT_INTERVAL}.zip"
    print(f"Checkpoint saved: {checkpoint_path}")

# Final save
model.save(MODEL_PATH)
print(f"Training complete! Model saved at {MODEL_PATH}")
