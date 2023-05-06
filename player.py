import math
import random

import settings


class SnakeDeath(Exception):
    """Thrown if snake dies"""


class Snake:
    def __init__(self, name, color, left_key, right_key, screen, clock):
        self.name = name
        self.x = random.randint(settings.START_MARGIN, settings.SCREEN_WIDTH - settings.START_MARGIN)
        self.y = random.randint(settings.START_MARGIN, settings.SCREEN_HEIGHT - settings.START_MARGIN)
        self.color = color
        self.angle = random.randint(0, 360)
        self.left_key = left_key
        self.right_key = right_key
        self.screen = screen
        self.clock = clock
        self.death = False
        self.hole = random.randint(*settings.HOLE_FREQUENCY_RANGE)
        self.hole_width = random.randint(*settings.HOLE_WIDTH_RANGE)

    def drive(self, keys, lines):
        if keys[self.left_key]:
            self.angle += settings.ANGLE_DELTA
        if keys[self.right_key]:
            self.angle -= settings.ANGLE_DELTA

        speed = self.clock.tick(60) / settings.SPEED_PER_FRAME
        nx = self.x + speed * math.cos(math.radians(-self.angle))
        ny = self.y + speed * math.sin(math.radians(-self.angle))

        self.check(nx, ny)

        if self.hole >= 0:
            lines.append((self.screen, self.color, (self.x, self.y), (nx, ny), settings.LINE_WIDTH))

        if self.hole == -self.hole_width:
            self.hole = random.randint(*settings.HOLE_FREQUENCY_RANGE)
            self.hole_width = random.randint(*settings.HOLE_WIDTH_RANGE)

        self.x = nx
        self.y = ny
        self.hole -= 1

    def check(self, nx, ny):
        if nx < 0:
            self.death = True
            return
        if nx > settings.SCREEN_WIDTH:
            self.death = True
            return
        if ny < 0:
            self.death = True
            return
        if ny > settings.SCREEN_HEIGHT:
            self.death = True
            return

        try:
            back_color = self.screen.get_at((round(nx), round(ny)))
        except IndexError:
            self.death = True
            return
        if back_color != settings.SCREEN_BACKGROUND_COLOR:
            self.death = True
            return

    def restart(self):
        self.death = False
        self.x = random.randint(settings.START_MARGIN, settings.SCREEN_WIDTH - settings.START_MARGIN)
        self.y = random.randint(settings.START_MARGIN, settings.SCREEN_HEIGHT - settings.START_MARGIN)
