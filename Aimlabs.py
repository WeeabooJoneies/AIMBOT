import pygame
from pygame.locals import *
import math
import random
import sys
import numpy as np
from collections import deque
from keras import layers
import tensorflow as tf
import time

# Define the DQN class
class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount factor
        self.epsilon = 1.0  # exploration factor (adjust as needed)
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()
        self.last_action_time = 0

    def build_model(self):
        model = tf.keras.Sequential()
        model.add(layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(layers.Dense(24, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=0.001))
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

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
                target = reward + self.gamma * np.amax(self.target_model.predict(next_state)[0])
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
    colors = np.array([blue, red, green])  # Convert to a 1-dimensional array

    clock = pygame.time.Clock()

    cx = random.randint(circle_size, width - circle_size)
    cy = random.randint(circle_size, height - circle_size)
    width_of_circle = circle_size
    circle_color = random.choice(colors)
    pygame.draw.circle(display, circle_color, (cx, cy), width_of_circle)

    # Initialize DQN agent
    state_size = 6  # cx, cy, score, misses, color index, mouse y-coordinate
    action_size = 9  # Move in 8 directions or not move
    agent = DQN(state_size, action_size)

    state = np.array([[cx, cy, score, misses, np.where(colors == circle_color)[0][0], 0]])  # Initialize state

    action = 0  # Initialize action

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    sqx = (x - cx) ** 2
                    sqy = (y - cy) ** 2
                    distance = math.sqrt(sqx + sqy)
                    if distance < width_of_circle:
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
                    next_state = np.array([[cx, cy, score, misses, np.where(colors == circle_color)[0][0], 0]])

                    # Remember the experience
                    done = False
                    agent.remember(state, action, reward, next_state, done)

                    # Train the DQN agent
                    agent.replay(batch_size=32)

                    # Get current state
                    state = next_state
                    action = agent.act(state)  # Update the agent's action based on the new state

        current_time = time.time()
        if current_time - agent.last_action_time >= 5:
            reward = -1  # Timeout, circle missed
            misses += 1
            print(f'Misses: {misses}')
            cx = random.randint(circle_size, width - circle_size)
            cy = random.randint(circle_size, height - circle_size)
            circle_color = random.choice(colors)
            agent.last_action_time = current_time

            # Update next state
            next_state = np.array([[cx, cy, score, misses, np.where(colors == circle_color)[0][0], 0]])

            # Remember the experience
            done = False
            agent.remember(state, action, reward, next_state, done)

            # Train the DQN agent
            agent.replay(batch_size=32)

            # Get current state
            state = next_state
            action = agent.act(state)  # Update the agent's action based on the new state
        else:
            # Move the mouse based on the AI's action
            if action == 0:  # Move left
                x, y = pygame.mouse.get_pos()
                x -= 5  # Adjust the x-coordinate to move the mouse left
                if x < 0:
                    x = 0  # Check if the mouse goes off the screen
                pygame.mouse.set_pos((x, y))
            elif action == 1:  # Move right
                x, y = pygame.mouse.get_pos()
                x += 5  # Adjust the x-coordinate to move the mouse right
                if x >= width:
                    x = width - 1
                pygame.mouse.set_pos((x, y))
            elif action == 2:  # Move up
                x, y = pygame.mouse.get_pos()
                y -= 5  # Adjust the y-coordinate to move the mouse up
                if y < 0:
                    y = 0
                pygame.mouse.set_pos((x, y))
            elif action == 3:  # Move down
                x, y = pygame.mouse.get_pos()
                y += 5  # Adjust the y-coordinate to move the mouse down
                if y >= height:
                    y = height - 1
                pygame.mouse.set_pos((x, y))
            elif action == 4:  # Move diagonally top-left
                x, y = pygame.mouse.get_pos()
                x -= 5
                y -= 5
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0
                pygame.mouse.set_pos((x, y))
            elif action == 5:  # Move diagonally top-right
                x, y = pygame.mouse.get_pos()
                x += 5
                y -= 5
                if x >= width:
                    x = width - 1
                if y < 0:
                    y = 0
                pygame.mouse.set_pos((x, y))
            elif action == 6:  # Move diagonally bottom-left
                x, y = pygame.mouse.get_pos()
                x -= 5
                y += 5
                if x < 0:
                    x = 0
                if y >= height:
                    y = height - 1
                pygame.mouse.set_pos((x, y))
            elif action == 7:  # Move diagonally bottom-right
                x, y = pygame.mouse.get_pos()
                x += 5
                y += 5
                if x >= width:
                    x = width - 1
                if y >= height:
                    y = height - 1
                pygame.mouse.set_pos((x, y))

        display.fill(black)
        pygame.draw.circle(display, circle_color, (cx, cy), width_of_circle)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    pygame.init()
    circle_size = int(sys.argv[1])
    resolution = (int(sys.argv[2]), int(sys.argv[3]))
    run_game(circle_size, resolution)