import pygame
from pygame.locals import *
import math
import random
import sys

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
    pygame.draw.circle(display, random.choice(colors), (cx, cy), width_of_circle)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pressed()
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                sqx = (x - cx)**2
                sqy = (y - cy)**2
                if math.sqrt(sqx + sqy) < width_of_circle and click[0] == 1:
                    score += 1
                    print(f'Score:{score}')
                    cx = random.randint(circle_size, width - circle_size)
                    cy = random.randint(circle_size, height - circle_size)
                    width_of_circle = circle_size
                    display.fill(black)
                    pygame.draw.circle(display, random.choice(colors), (cx, cy), width_of_circle)
                elif click[0] == 1 and not math.sqrt(sqx + sqy) < width_of_circle:
                    misses += 1
                    print(f'Misses:{misses}')
                    cx = random.randint(circle_size, width - circle_size)
                    cy = random.randint(circle_size, height - circle_size)
                    width_of_circle = circle_size
                    display.fill(black)
                    pygame.draw.circle(display, random.choice(colors), (cx, cy), width_of_circle)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    circle_size = 30
    resolution = (800, 600)
    pygame.init()
    run_game(circle_size, resolution)