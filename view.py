import pygame
import numpy as np
from settings import *


class View:
    def __init__(self, count_envs):
        self.width = count_envs * (GAME_WIDTH + CELL) + CELL
        self.height = 980
        self.screen = pygame.display.set_mode((self.width, self.height))

    def fill(self, color):
        self.screen.fill(color)

    def draw_text(self, text, pos, size, color, font_name, make_centered_w=False, make_centered_h=False):
        # define font
        font = pygame.font.SysFont(font_name, size)
        # render font
        on_screen_text = font.render(text, False, color)
        # place at pos
        if make_centered_w:
            pos[0] = pos[0] - on_screen_text.get_size()[0] // 2
        if make_centered_h:
            pos[1] = pos[1] - on_screen_text.get_size()[1] // 2
        self.screen.blit(on_screen_text, pos)

    def draw_grid(self, x0, y0, width, height, count_x, count_y):
        # Grid top-bottom
        for i in range(1, count_x):
            pygame.draw.line(self.screen, COLOR_LIGHT_GRAY,
                             (x0 + i * CELL, y0),
                             (x0 + i * CELL, y0 + height))
        # Grid left-right
        for i in range(1, count_y):
            pygame.draw.line(self.screen, COLOR_LIGHT_GRAY,
                             (x0, y0 + i * CELL),
                             (x0 + width, y0 + i * CELL))

    def draw_box(self, x0, y0, width, height, color, border_width=1):
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(x0 - border_width, y0 - border_width,
                                     width + border_width, height + border_width), border_width)