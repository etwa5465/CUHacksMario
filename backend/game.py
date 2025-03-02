import gym
import cv2
import numpy as np
from gym_super_mario_bros import make
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

class MarioGame:
    def __init__(self, render_mode="human"):
        self.env = make("SuperMarioBros-1-1-v0", apply_api_compatibility=True, render_mode=render_mode)
        self.env = gym.wrappers.GrayScaleObservation(self.env, keep_dim=True)
        self.env.reset()

    def play_human(self):
        done = False
        obs, _ = self.env.reset()
        while not done:
            action = self.env.action_space.sample()  # Replace with user input if needed
            obs, reward, terminated, truncated, _ = self.env.step(action)
            self.render_frame(obs)
            done = terminated or truncated

    def render_frame(self, obs):
        frame = np.array(obs)
        frame = cv2.resize(frame, (512, 512))
        cv2.imshow("Mario AI", frame)
        cv2.waitKey(1)

    def close(self):
        self.env.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    game = MarioGame()
    game.play_human()
    game.close()
