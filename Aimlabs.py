import pygame
from pygame.locals import *
import math
import random
import sys
import numpy as np
import tensorflow as tf
from keras import layers
import time

# Define the DQN class
class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95  # discount factor
        self.epsilon = 0.5  # exploration factor (adjust as needed)
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self.build_model()
        self.last_action_time = 0

    def build_model(self):
        model = tf.keras.Sequential()
        model.add(layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(layers.Dense(24, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=0.001))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

 
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])


    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def run_game(circle_size, resolution):
    score = 0
    misses = 0
    width, height = resolution
    display = pygame.display.set_mode(resolution)
    black = (0, 0, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 200, 0)
    colors = [blue, red, green]

    clock = pygame.time.Clock()

    cx = random.randint(circle_size, width - circle_size)
    cy = random.randint(circle_size, height - circle_size)
    width_of_circle = circle_size
    circle_color = random.choice(colors)
    pygame.draw.circle(display, circle_color, (cx, cy), width_of_circle)

    # Initialize DQN agent
    state_size = 5  # cx, cy, score, misses, color index
    action_size = 2  # Move or not move
    agent = DQN(state_size, action_size)

    state = np.array([[cx, cy, score, misses, colors.index(circle_color)]])  # Initialize state

    action = 0  # Initialize action

    last_click_time = pygame.time.get_ticks()
    click_cooldown = 500

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move the mouse based on the AI's action
        if action == 1:
            x, y = pygame.mouse.get_pos()
            x += 5  # Adjust the x-coordinate to move the mouse right
            pygame.mouse.set_pos((x, y))

        # Check for mouse button clicks
        click = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        sqx = (x - cx) ** 2
        sqy = (y - cy) ** 2

        if math.sqrt(sqx + sqy) < width_of_circle and (click[0] == 1 or click[2] == 1):
            reward = 1  # Circle clicked
            score += 1
            print(f'Score: {score}')
            cx = random.randint(circle_size, width - circle_size)
            cy = random.randint(circle_size, height - circle_size)
            circle_color = random.choice(colors)
            agent.last_action_time = time.time()
        else:
            reward = -1  # Circle missed
            misses += 1
            print(f'Misses: {misses}')
            cx = random.randint(circle_size, width - circle_size)
            cy = random.randint(circle_size, height - circle_size)
            circle_color = random.choice(colors)
            agent.last_action_time = time.time()

        # Update next state
        next_state = np.array([[cx, cy, score, misses, colors.index(circle_color)]])

        # Remember the experience
        done = False
        agent.remember(state, action, reward, next_state, done)

        # Train the DQN agent
        agent.replay(batch_size=32)

        # Get current state
        state = np.array([[cx, cy, score, misses, colors.index(circle_color)]])
        action = agent.act(state)
        # DQN agent selects an action
        
        # Update the display
        display.fill(black)
        pygame.draw.circle(display, circle_color, (cx, cy), width_of_circle)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    pygame.init()
    circle_size = int(sys.argv[1])
    resolution = (int(sys.argv[2]), int(sys.argv[3]))
    run_game(circle_size, resolution)
