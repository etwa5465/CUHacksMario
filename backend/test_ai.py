import gymnasium as gym
from stable_baselines3 import PPO
from mario_env import MarioEnv
import pygame

# Initialize Pygame
pygame.init()

# Create environment with "human" render mode to view gameplay
env = MarioEnv(render_mode="human")  # Ensure this renders the game to the screen

# Load the trained model
model = PPO.load("mario_ai_model")

# Initialize the environment and get the first observation
obs, info = env.reset()

done = False

# Start the event loop for Pygame to prevent freezing and handle user events
while not done:
    for event in pygame.event.get():  # Check for any events (like closing the window)
        if event.type == pygame.QUIT:
            done = True  # Exit the loop if the user closes the window

    # Get action from the model
    action, _states = model.predict(obs)

    # Take the action in the environment
    obs, reward, done, _, info = env.step(action)

    # Render the game
    env.render()

    # Explicitly update the display (important for some systems)
    pygame.display.update()

# Close the environment and Pygame window
env.close()
pygame.quit()
