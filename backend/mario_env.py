import gym
import numpy as np
import cv2
from gym import spaces

class CustomMarioEnv(gym.Env):
    def __init__(self):
        super(CustomMarioEnv, self).__init__()

        # ✅ Level parameters
        self.width = 800
        self.height = 600
        self.mario_x = 50
        self.mario_y = 500
        self.goomba_x = 400
        self.goomba_y = 500
        self.goal_x = 750
        self.goal_y = 500
        self.platforms = [(300, 450, 100, 10), (500, 400, 100, 10)]  # (x, y, width, height)

        # ✅ Rendering setup
        self.frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # ✅ Gym setup
        self.action_space = spaces.Discrete(3)  # Left, Right, Jump
        self.observation_space = spaces.Box(low=0, high=255, shape=(84, 84, 1), dtype=np.uint8)

        self.reset()

    def reset(self):
        """Reset Mario, Goomba, and game state"""
        self.mario_x = 50
        self.mario_y = 500
        self.goomba_x = 400
        self.goomba_y = 500
        self.done = False
        return self._get_obs()

    def step(self, action):
        """Move Mario based on action"""
        if action == 0:
            self.mario_x -= 5  # Move left
        elif action == 1:
            self.mario_x += 5  # Move right
        elif action == 2 and self._on_ground():
            self.mario_y -= 50  # Jump

        # ✅ Apply gravity
        self.mario_y += 5  

        # ✅ Ensure Mario does NOT leave screen bounds
        self.mario_x = max(0, min(self.width - 20, self.mario_x))  # Keep Mario within screen
        if self.mario_y > 500:  
            self.mario_y = 500  # Keep Mario on the ground

        # ✅ If Mario falls off the screen, he dies
        if self.mario_y >= self.height:
            self.done = True
            reward = -100  # Big penalty for falling
            return self._get_obs(), reward, self.done, {}

        # ✅ Check if Mario lands on a platform
        for px, py, pw, ph in self.platforms:
            if px <= self.mario_x <= px + pw and py - 10 <= self.mario_y <= py + ph:
                self.mario_y = py - 5  # Land on platform

        # ✅ Move Goomba back and forth
        self.goomba_x += np.random.choice([-2, 2])  
        self.goomba_x = max(300, min(500, self.goomba_x))  # Keep within range
        GOOMBA_WIDTH, GOOMBA_HEIGHT = 20, 20  # Define Goomba size
        MARIO_WIDTH, MARIO_HEIGHT = 20, 20  # Define Mario size

        # ✅ More precise collision detection (bounding box check)
        if (self.mario_x < self.goomba_x + GOOMBA_WIDTH and
            self.mario_x + MARIO_WIDTH > self.goomba_x and
            self.mario_y < self.goomba_y + GOOMBA_HEIGHT and
            self.mario_y + MARIO_HEIGHT > self.goomba_y):
            self.done = True
            reward = -100  # Big penalty for touching the Goomba
            print("💀 Mario collided with Goomba! Resetting...")

        # ✅ Check collision with Goomba (Game Over)
        if abs(self.mario_x - self.goal_x) < 20:  # ✅ Goal Reached
            self.done = True
            reward = 100  # Huge reward for reaching goal
        elif self.mario_x > 50:  
            reward = 5  # ✅ Strong reward for moving right
        elif self.mario_x < 50:  
            reward = -5  # ❌ Strong penalty for moving left
        elif abs(self.mario_x - self.goomba_x) < 20 and abs(self.mario_y - self.goomba_y) < 20:
            self.done = True
            reward = -50
        elif abs(self.mario_x - self.goomba_x) < 50:  
            reward -= 5
        else:
            reward = -1  # Neutral reward for staying still


        return self._get_obs(), reward, self.done, {}

    def _on_ground(self):
        """Check if Mario is on the ground or a platform"""
        if self.mario_y >= 500:
            return True
        for px, py, pw, ph in self.platforms:
            if px <= self.mario_x <= px + pw and py - 10 <= self.mario_y <= py + ph:
                return True
        return False

    def render(self):
        """Render the level with Mario, Goomba, platforms, and goal"""
        self.frame[:] = (0, 0, 0)  # Background
        cv2.rectangle(self.frame, (self.mario_x, self.mario_y), (self.mario_x + 20, self.mario_y + 20), (0, 0, 255), -1)  # Mario
        cv2.rectangle(self.frame, (self.goomba_x, self.goomba_y), (self.goomba_x + 20, self.goomba_y + 20), (0, 165, 255), -1)  # Goomba
        cv2.rectangle(self.frame, (self.goal_x, self.goal_y), (self.goal_x + 20, self.goal_y + 20), (0, 255, 0), -1)  # Goal
        
        # Draw platforms
        for px, py, pw, ph in self.platforms:
            cv2.rectangle(self.frame, (px, py), (px + pw, py + ph), (255, 255, 255), -1)  

    def _get_obs(self):
        """Get AI's grayscale view of the game"""
        gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray_frame, (84, 84), interpolation=cv2.INTER_AREA)
        return resized_frame.reshape(84, 84, 1)

    def get_frame(self):
        """Return frame for frontend"""
        return cv2.resize(self.frame, (512, 512))
