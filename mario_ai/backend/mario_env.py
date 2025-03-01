import gymnasium as gym
import pygame
import numpy as np
from gymnasium import spaces

class MarioEnv(gym.Env):
    def __init__(self, render_mode="rgb_array"):
        super().__init__()

        self.render_mode = render_mode
        self.width = 800
        self.height = 600

        # Define the action and observation space
        self.action_space = spaces.Discrete(4)  # Example: move left, right, jump, etc.
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.height, self.width, 3), dtype=np.uint8)

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Super Mario AI")

        # Initialize Mario's position
        self.mario = pygame.Rect(100, 500, 50, 50)  # Example Mario as a rectangle

    def reset(self):
        self.mario.x = 100
        self.mario.y = 500
        self.screen.fill((255, 255, 255))  # Clear screen with white
        return np.zeros((self.height, self.width, 3), dtype=np.uint8)

    def step(self, action):
        reward = 0
        done = False

        # Example Mario movement (you can adjust the logic here)
        if action == 0:  # Move left
            self.mario.x -= 5
        elif action == 1:  # Move right
            self.mario.x += 5
        elif action == 2:  # Jump (change y position)
            self.mario.y -= 10
        elif action == 3:  # Duck (change y position)
            self.mario.y += 10

        # Check for out-of-bound conditions (for demo purposes)
        if self.mario.x < 0:
            self.mario.x = 0
        if self.mario.x > self.width - self.mario.width:
            self.mario.x = self.width - self.mario.width
        if self.mario.y > self.height - self.mario.height:
            self.mario.y = self.height - self.mario.height

        # Example condition for ending the game
        if self.mario.y < 0:
            done = True
            reward = 100  # Give reward when Mario reaches the top (just for demo)

        # Drawing Mario
        self.screen.fill((255, 255, 255))  # Fill the screen with white
        pygame.draw.rect(self.screen, (0, 0, 255), self.mario)  # Draw Mario as a blue rectangle

        # If render_mode is human, update the display
        if self.render_mode == "human":
            pygame.display.update()

        return np.array(self.screen), reward, done, {}

    def render(self):
        # This will update the Pygame window based on the screen object
        if self.render_mode == "human":
            pygame.display.update()
        return self.screen

# import gymnasium as gym
# import pygame
# import numpy as np

# class MarioEnv(gym.Env):
#     """Custom Gym environment for our Pygame Mario game."""
#     metadata = {"render_modes": ["human", "rgb_array"]}

#     def __init__(self, render_mode="rgb_array"):
#         super().__init__()

#         # Game Constants
#         self.WIDTH, self.HEIGHT = 800, 600
#         self.GRAVITY = 1
#         self.JUMP_STRENGTH = -15
#         self.SPEED = 5

#         self.render_mode = render_mode  # ✅ Store render mode

#         if self.render_mode == "human":
#             self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
#         else:
#             self.screen = pygame.Surface((self.WIDTH, self.HEIGHT))  # ✅ Off-screen surface for training

#         pygame.display.set_caption("Mario AI")

#         # Define Action & Observation Space
#         self.action_space = gym.spaces.Discrete(4)
#         self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)

#         # Initialize Game Objects
#         self.mario = pygame.Rect(100, 500, 40, 50)
#         self.ground = pygame.Rect(0, 550, self.WIDTH * 3, 50)
#         self.platforms = [
#             pygame.Rect(300, 450, 150, 20),
#             pygame.Rect(600, 350, 150, 20),
#             pygame.Rect(900, 250, 150, 20),
#             pygame.Rect(1200, 450, 150, 20),
#         ]
#         self.flagpole = pygame.Rect(1500, 450, 20, 100)

#         self.velocity_y = 0
#         self.on_ground = False

#     def step(self, action):
#         """Executes one game step based on the AI's action."""

#         if action == 1:  # Move Left
#             self.mario.x -= self.SPEED
#         elif action == 2:  # Move Right
#             self.mario.x += self.SPEED
#         elif action == 3 and self.on_ground:  # Jump
#             self.velocity_y = self.JUMP_STRENGTH
#             self.on_ground = False

#         # Apply Gravity
#         self.velocity_y += self.GRAVITY
#         self.mario.y += self.velocity_y

#         # Collision with Ground
#         if self.mario.colliderect(self.ground):
#             self.mario.y = self.ground.y - self.mario.height
#             self.velocity_y = 0
#             self.on_ground = True

#         # Collision with Platforms (Prevents Jumping Through)
#         for platform in self.platforms:
#             if self.mario.colliderect(platform):
#                 # ✅ Block Mario if he is falling onto the platform
#                 if self.velocity_y > 0 and self.mario.bottom > platform.top:
#                     self.mario.y = platform.y - self.mario.height
#                     self.velocity_y = 0
#                     self.on_ground = True
#                 # ✅ Prevent Mario from passing through from below
#                 elif self.velocity_y < 0 and self.mario.top < platform.bottom:
#                     self.mario.y = platform.bottom
#                     self.velocity_y = 0  # Stop upward movement

#         # ✅ Ensure Mario doesn't fall off the screen
#         if self.mario.y > self.HEIGHT:
#             done = True
#             reward = -10  # Penalty for falling
#         elif self.mario.colliderect(self.flagpole):
#             reward = 100
#             done = True
#         else:
#             reward = 0.1  # Small reward for staying alive
#             done = False

#         obs = self._get_observation()
#         return obs, reward, done, False, {}

#     def reset(self, seed=None, options=None):
#         """Resets the game environment."""
#         self.mario = pygame.Rect(100, 500, 40, 50)
#         self.velocity_y = 0
#         self.on_ground = False
#         return self._get_observation(), {}

#     def _get_observation(self):
#         """Returns the current game screen as a NumPy array."""
#         pixels = pygame.surfarray.array3d(self.screen)
#         obs = np.transpose(pixels, (1, 0, 2))  # Convert to (height, width, channels)
#         return obs

#     def render(self, mode="human"):
#         """Renders the game."""
#         self.screen.fill((255, 255, 255))
#         pygame.draw.rect(self.screen, (0, 255, 0), self.ground)
#         pygame.draw.rect(self.screen, (255, 0, 0), self.mario)
#         pygame.draw.rect(self.screen, (0, 0, 255), self.flagpole)

#         for platform in self.platforms:
#             pygame.draw.rect(self.screen, (0, 255, 255), platform)

#         if self.render_mode == "human":
#             pygame.display.flip()

#     def close(self):
#         """Closes the game."""
#         pygame.quit()
