import time

import pygame
import numpy
from settings import *
from game_env.game_env import GameEnv

pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game_state = "start"
        self.running = True

        # start vars
        self.ai_difficulties = ["EASY", "MEDIUM", "HARD"]
        self.ai_l = 1
        self.ai_r = 1

        # play vars
        self.env = None
        self.play_inputs = 0

    def run(self):
        while self.running:
            if self.game_state == "start":
                self.start_events()
                self.start_update()
                self.start_draw()

            elif self.game_state == "play_load":
                self.play_load_draw()
                self.play_load_update()

            elif self.game_state == "play":
                self.play_events()
                self.play_update()
                self.play_draw()

            elif self.game_state == "end":
                self.end_events()
                self.end_update()
                self.end_draw()
            else:
                self.running = False

            pygame.display.update()
            self.clock.tick(FPS)
        else:
            pygame.quit()

#   START   START   START   START   START   START   START   START   START   START   START

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                # movement
                if event.key == pygame.K_SPACE:
                    self.game_state = "play_load"
                if event.key == pygame.K_a:
                    self.ai_l += 1
                    if self.ai_l == len(self.ai_difficulties):
                        self.ai_l = 0
                if event.key == pygame.K_d:
                    self.ai_r += 1
                    if self.ai_r == len(self.ai_difficulties):
                        self.ai_r = 0

    def start_update(self):
        pass

    def start_draw(self):
        # fill background
        self.screen.fill(COLOR_DARK_GRAY)

        self.draw_text("TETRIS",
                       [DISPLAY_WIDTH // 2, 70],
                       280, COLOR_YELLOW, DEFAULT_FONT, True, False)
        self.draw_text("B A T T L E   R O Y A L E",
                       [DISPLAY_WIDTH // 2, 250],
                       70, COLOR_RED, DEFAULT_FONT, True, False)

        self.draw_text("AGENT-L",
                       [DISPLAY_WIDTH // 2 - 240, 550],
                       60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.draw_text("AI: " + self.ai_difficulties[self.ai_l],
                       [DISPLAY_WIDTH // 2 - 240, 600],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.draw_text("[A] TO CHANGE",
                       [DISPLAY_WIDTH // 2 - 240, 640],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("|",
                       [DISPLAY_WIDTH // 2 - 100, 590],
                       155, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("PRESS",
                       [DISPLAY_WIDTH // 2, 550],
                       60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.draw_text("[SPACE]",
                       [DISPLAY_WIDTH // 2, 600],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.draw_text("TO PLAY",
                       [DISPLAY_WIDTH // 2, 640],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("|",
                       [DISPLAY_WIDTH // 2 + 100, 590],
                       155, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("AGENT-R",
                       [DISPLAY_WIDTH // 2 + 240, 550],
                       60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.draw_text("AI: " + self.ai_difficulties[self.ai_r],
                       [DISPLAY_WIDTH // 2 + 240, 600],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.draw_text("[D] TO CHANGE",
                       [DISPLAY_WIDTH // 2 + 240, 640],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("By Dmytro Geleshko",
                       [40, DISPLAY_HEIGHT - 40],
                       30, COLOR_WHITE, DEFAULT_FONT, False, False)

#   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD

    def play_load_draw(self):
        self.screen.fill(COLOR_DARK_GRAY)

        self.draw_text("LOADING...",
                       [DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2],
                       128, COLOR_WHITE, DEFAULT_FONT, True, True)

        pygame.display.update()

    def play_load_update(self):
        self.game_envs = [GameEnv() for _ in range(3)]
        print(self.game_envs[0].map)
        self.game_state = "play"

#   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY   PLAY   PLAY

    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.play_inputs = 1
                if event.key == pygame.K_d:
                    self.play_inputs = 2
                if event.key == pygame.K_s:
                    self.play_inputs = 3
                if event.key == pygame.K_w:
                    self.play_inputs = 4

    def play_update(self):
        #self.env.step(self.play_inputs)
        pass

    def play_draw(self):
        self.screen.fill(COLOR_DARK_GRAY)

        self.draw_text("TETRIS",
                       [150, 15],
                       180, COLOR_YELLOW, DEFAULT_FONT, False, False)
        self.draw_text("BATTLE",
                       [750, 15],
                       80, COLOR_RED, DEFAULT_FONT, True, False)
        self.draw_text("ROYALE",
                       [750, 75],
                       80, COLOR_RED, DEFAULT_FONT, True, False)

        self.draw_text("AGENT-L",
                       [180, 165],
                       60, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("PLAYER",
                       [510, 165],
                       60, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("AGENT-R",
                       [840, 165],
                       60, COLOR_WHITE, DEFAULT_FONT, True, True)
        for i in range(3):
            x0 = i * GAME_WIDTH + (i + 1) * CELL

            self.draw_grid(x0, TOP_OFFSET, GAME_WIDTH, GAME_HEIGHT, GAME_MAP_WIDTH, GAME_MAP_HEIGHT)
            self.draw_box(x0, TOP_OFFSET, GAME_WIDTH, GAME_HEIGHT, COLOR_RED, 3)

#   END   END   END   END   END   END   END   END   END   END   END   END   END   END   END   END   END

    def end_events(self):
        pass

    def end_update(self):
        pass

    def end_draw(self):
        pass

#   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT

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
                         pygame.Rect(x0, y0,
                                     width, height), border_width)
