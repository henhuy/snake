import time

import pygame

import player
import settings


pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

snakes = [
    player.Snake(
        "Janne",
        "red",
        pygame.K_n,
        pygame.K_m,
        screen,
        clock,
    ),
    player.Snake(
        "Henner",
        "orange",
        pygame.K_a,
        pygame.K_s,
        screen,
        clock,
    ),
]
lines = []

paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(settings.SCREEN_BACKGROUND_COLOR)

    for line in lines:
        pygame.draw.line(*line)

    keys = pygame.key.get_pressed()

    deaths = sum(snake.death for snake in snakes)
    if deaths >= len(snakes) - 1:
        if not paused:
            for snake in snakes:
                if not snake.death:
                    msg = f"{snake.name} gewinnt!"
                    print(msg)
        paused = True

        if keys[pygame.K_SPACE]:
            paused = False
            lines = []
            for snake in snakes:
                snake.restart()
            continue

    for snake in snakes:
        if snake.death:
            continue
        snake.drive(keys, lines)

    pygame.display.flip()

time.sleep(2)
pygame.quit()
