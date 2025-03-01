import gymnasium as gym
import pygame
import numpy as np
from gymnasium import spaces

class MarioEnv(gym.Env):
    def __init__(self, render_mode="rgb_array"):
        super().__init__()

        self.width = 800
        self.height = 600
        self.render_mode = render_mode

        # Define action space (move left, right, jump)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.height, self.width, 3), dtype=np.uint8)

        # Pygame setup (off-screen rendering)
        pygame.init()
        self.screen = pygame.Surface((self.width, self.height))  # Headless Mode
        self.mario = pygame.Rect(100, 500, 50, 50)

    def step(self, action):
        reward = 0
        done = False

        if action == 1:  # Move Left
            self.mario.x -= 5
        elif action == 2:  # Move Right
            self.mario.x += 5
        elif action == 3:  # Jump
            self.mario.y -= 10

        if self.mario.y < 0:  # Example win condition
            done = True
            reward = 100

        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 255), self.mario)  # Draw Mario

        return self._get_observation(), reward, done, False, {}

    def render(self):
        return pygame.surfarray.array3d(self.screen)

    def reset(self, seed=None, options=None):
        self.mario.x = 100
        self.mario.y = 500
        return self._get_observation(), {}

    def _get_observation(self):
        return np.transpose(pygame.surfarray.array3d(self.screen), (1, 0, 2))
