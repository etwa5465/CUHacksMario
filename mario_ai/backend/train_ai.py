import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.policies import ActorCriticCnnPolicy  # ✅ Add this import
from mario_env import MarioEnv

# ✅ Print debug message before environment creation
print("🛠️ Creating Mario Environment...")

# ✅ Create environment WITHOUT opening a Pygame window
env = MarioEnv(render_mode="rgb_array")

# ✅ Print message before PPO initialization
print("🚀 Initializing PPO Model...")

# ✅ Train AI using PPO
model = PPO(
    ActorCriticCnnPolicy,
    env,
    verbose=1,
    n_steps=100,  # ✅ Train for exactly 100 steps
    n_epochs=1,   # ✅ Ensure PPO doesn't over-optimize
)

# ✅ Print message before training starts
print("🎮 Starting AI Training...")

# ✅ Train for a fixed number of timesteps with a progress bar
model.learn(total_timesteps=100, progress_bar=True)

# ✅ Print message when training completes
print("✅ Training Complete. Saving model...")

# ✅ Save the trained model
model.save("mario_ai_model")

print("💾 AI Model Saved!")
