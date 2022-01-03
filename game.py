import time
from agent_rl.agent import Agent
import pygame
import numpy as np
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
        self.game_envs = None
        self.agent_l = None
        self.play_inputs = 0
        self.scores = None

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
        self.agent_l = Agent()
        self.agent_l.build_model()
        self.agent_l.build_agent()
        self.agent_l.compile()
        self.agent_l.load_model_weights(r"agent_rl/saved/dqn_v2.h5")

        self.game_envs = [GameEnv() for _ in range(3)]
        self.scores = [0, 0, 0]
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
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "end"

    def play_update(self):
        all_stopped = True
        for game in self.game_envs:
            if game.running:
                all_stopped = False
                break
        if all_stopped:
            self.game_state = "end"
            return

        # AGENT-L
        action = self.agent_l.get_action(self.game_envs[0].map, self.game_envs[0].shape, self.game_envs[0].next_shape)
        self.scores[0] += self.game_envs[0].step(action)

        # PLAYER
        self.scores[1] += self.game_envs[1].step(self.play_inputs)
        self.play_inputs = 0

        # AGENT-R
        self.scores[2] += self.game_envs[2].step(np.random.randint(0, 5))


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
            game_field_x = i * GAME_WIDTH + (i + 1) * CELL
            game_field_y = TOP_OFFSET

            # game fields
            self.draw_grid(game_field_x, game_field_y,
                           GAME_WIDTH, GAME_HEIGHT,
                           GAME_SHAPE_WIDTH, GAME_SHAPE_HEIGHT)
            self.draw_box(game_field_x, game_field_y,
                          GAME_WIDTH, GAME_HEIGHT,
                          COLOR_RED, 3)
            # draw locked
            for map_x in range(GAME_SHAPE_WIDTH):
                for map_y in range(GAME_SHAPE_HEIGHT):
                    if self.game_envs[i].at(map_x, map_y):
                        pygame.draw.rect(self.screen, COLOR_LIGHT_GRAY,
                                         pygame.Rect(game_field_x + map_x * CELL, game_field_y + map_y * CELL,
                                                     CELL, CELL))
            # draw figure
            for figure_x in range(NEXT_SHAPE_WIDTH):
                for figure_y in range(NEXT_SHAPE_HEIGHT):
                    figure_x0 = self.game_envs[i].shape.x
                    figure_y0 = self.game_envs[i].shape.y - 1
                    if figure_y0 + figure_y > GAME_SHAPE_TOP_HIDDEN \
                            and self.game_envs[i].shape.at(figure_x, figure_y) == 1:
                        pygame.draw.rect(self.screen,  self.game_envs[i].shape.color,
                                         pygame.Rect(game_field_x
                                                     + (figure_x0 + figure_x - GAME_SHAPE_BORDERS) * CELL,
                                                     game_field_y
                                                     + int((figure_y0 + figure_y - GAME_SHAPE_TOP_HIDDEN) * CELL),
                                                     CELL, CELL))
            # next fields
            next_field_x = game_field_x + GAME_WIDTH - NEXT_WIDTH
            next_field_y = game_field_y + GAME_HEIGHT + CELL

            # scores
            self.draw_text("SCORE",
                           [game_field_x, next_field_y],
                           60, COLOR_WHITE, DEFAULT_FONT, False, False)
            self.draw_text(str(self.scores[i]),
                           [game_field_x, next_field_y + 60],
                           60, COLOR_WHITE, DEFAULT_FONT, False, False)

            self.draw_grid(next_field_x, next_field_y,
                           NEXT_WIDTH, NEXT_HEIGHT,
                           NEXT_SHAPE_WIDTH, NEXT_SHAPE_HEIGHT)
            self.draw_box(next_field_x, next_field_y,
                          NEXT_WIDTH, NEXT_HEIGHT,
                          COLOR_RED, 3)
            for next_x in range(NEXT_SHAPE_WIDTH):
                for next_y in range(NEXT_SHAPE_HEIGHT):
                    if self.game_envs[i].next_shape.at(next_x, next_y) == 1:
                        pygame.draw.rect(self.screen,  self.game_envs[i].next_shape.color,
                                         pygame.Rect(next_field_x + next_x * CELL, next_field_y + next_y * CELL,
                                                     CELL, CELL))
            if not self.game_envs[i].running:
                pygame.draw.line(self.screen, COLOR_RED,
                                 (game_field_x, game_field_y),
                                 (game_field_x + GAME_WIDTH, game_field_y + GAME_HEIGHT), 3)
                pygame.draw.line(self.screen, COLOR_RED,
                                 (game_field_x + GAME_WIDTH, game_field_y),
                                 (game_field_x, game_field_y + GAME_HEIGHT), 3)

#   END   END   END   END   END   END   END   END   END   END   END   END   END   END   END   END   END

    def end_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game_state = "start"

    def end_update(self):
        pass

    def end_draw(self):
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
        self.draw_text("SCORE: " + str(self.scores[0]),
                       [DISPLAY_WIDTH // 2 - 240, 640],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("|",
                       [DISPLAY_WIDTH // 2 - 100, 590],
                       155, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("PLAYER",
                       [DISPLAY_WIDTH // 2, 550],
                       60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.draw_text("SCORE: " + str(self.scores[1]),
                       [DISPLAY_WIDTH // 2, 600],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("PRESS",
                       [DISPLAY_WIDTH // 2, 750],
                       60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.draw_text("[SPACE]",
                       [DISPLAY_WIDTH // 2, 800],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.draw_text("TO PLAY",
                       [DISPLAY_WIDTH // 2, 840],
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
        self.draw_text("SCORE: " + str(self.scores[2]),
                       [DISPLAY_WIDTH // 2 + 240, 640],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)

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
                         pygame.Rect(x0 - border_width, y0 - border_width,
                                     width + border_width, height + border_width), border_width)
