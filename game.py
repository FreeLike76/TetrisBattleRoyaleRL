import time
from view import View
import pygame
import numpy as np
from settings import *
from game_env.game_env import GameEnv

pygame.init()


class Game:
    def __init__(self, agents):

        self.agents_names = []
        self.agents = []
        for name, agent in agents.items():
            self.agents_names.append(name)
            self.agents.append(agent)

        self.view = View(len(agents) + 1)

        self.clock = pygame.time.Clock()

        self.game_state = "start"
        self.running = True

        # play vars
        self.game_envs = None
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

    def start_update(self):
        pass

    def start_draw(self):
        # fill background
        self.view.fill(COLOR_DARK_GRAY)

        self.view.draw_text("TETRIS",
                            [self.view.width // 2, 70],
                            280, COLOR_YELLOW, DEFAULT_FONT, True, False)
        self.view.draw_text("B A T T L E   R O Y A L E",
                            [self.view.width // 2, 250],
                            70, COLOR_RED, DEFAULT_FONT, True, False)

        self.view.draw_text("|",
                            [self.view.width // 2 - 100, 590],
                            155, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.view.draw_text("PRESS",
                            [self.view.width // 2, 550],
                            60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.view.draw_text("[SPACE]",
                            [self.view.width // 2, 600],
                            35, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.view.draw_text("TO PLAY",
                            [self.view.width // 2, 640],
                            35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.view.draw_text("|",
                            [self.view.width // 2 + 100, 590],
                            155, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.view.draw_text("By Dmytro Geleshko",
                            [40, self.view.height - 40],
                            30, COLOR_WHITE, DEFAULT_FONT, False, False)

    #   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD

    def play_load_draw(self):
        self.view.fill(COLOR_DARK_GRAY)

        self.view.draw_text("LOADING...",
                            [self.view.width // 2, self.view.height // 2],
                            128, COLOR_WHITE, DEFAULT_FONT, True, True)

        pygame.display.update()

    def play_load_update(self):
        self.game_envs = [GameEnv() for _ in range(len(self.agents) + 1)]
        self.scores = [0 for _ in range(len(self.game_envs))]
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

        for i in range(len(self.game_envs)):
            if i == 0:
                self.scores[i] += self.game_envs[i].step(self.play_inputs)
                self.play_inputs = 0
            else:
                self.scores[i] += self.game_envs[i].step(self.agents[i - 1].get_action(self.game_envs[i].map,
                                                                                       self.game_envs[i].shape,
                                                                                       self.game_envs[i].next_shape))

    def play_draw(self):
        self.view.fill(COLOR_DARK_GRAY)

        self.view.draw_text("TETRIS",
                            [150, 15],
                            180, COLOR_YELLOW, DEFAULT_FONT, False, False)
        self.view.draw_text("BATTLE",
                            [750, 15],
                            80, COLOR_RED, DEFAULT_FONT, True, False)
        self.view.draw_text("ROYALE",
                            [750, 75],
                            80, COLOR_RED, DEFAULT_FONT, True, False)

        for i in range(len(self.game_envs)):
            game_field_x = i * GAME_WIDTH + (i + 1) * CELL
            game_field_y = TOP_OFFSET
            if i == 0:
                self.view.draw_text("PLAYER",
                                    [game_field_x + GAME_WIDTH // 2, 165],
                                    60, COLOR_WHITE, DEFAULT_FONT, True, True)
            else:
                self.view.draw_text(self.agents_names[i - 1],
                                    [game_field_x + GAME_WIDTH // 2, 165],
                                    60, COLOR_WHITE, DEFAULT_FONT, True, True)
            # game fields
            self.view.draw_grid(game_field_x, game_field_y,
                                GAME_WIDTH, GAME_HEIGHT,
                                GAME_SHAPE_WIDTH, GAME_SHAPE_HEIGHT)
            self.view.draw_box(game_field_x, game_field_y,
                               GAME_WIDTH, GAME_HEIGHT,
                               COLOR_RED, 3)
            # draw locked
            for map_x in range(GAME_SHAPE_WIDTH):
                for map_y in range(GAME_SHAPE_HEIGHT):
                    if self.game_envs[i].at(map_x, map_y):
                        pygame.draw.rect(self.view.screen, COLOR_LIGHT_GRAY,
                                         pygame.Rect(game_field_x + map_x * CELL, game_field_y + map_y * CELL,
                                                     CELL, CELL))
            # draw figure
            for figure_x in range(NEXT_SHAPE_WIDTH):
                for figure_y in range(NEXT_SHAPE_HEIGHT):
                    figure_x0 = self.game_envs[i].shape.x
                    figure_y0 = self.game_envs[i].shape.y - 1
                    if figure_y0 + figure_y > GAME_SHAPE_TOP_HIDDEN \
                            and self.game_envs[i].shape.at(figure_x, figure_y) == 1:
                        pygame.draw.rect(self.view.screen, self.game_envs[i].shape.color,
                                         pygame.Rect(game_field_x
                                                     + (figure_x0 + figure_x - GAME_SHAPE_BORDERS) * CELL,
                                                     game_field_y
                                                     + int((figure_y0 + figure_y - GAME_SHAPE_TOP_HIDDEN) * CELL),
                                                     CELL, CELL))
            # next fields
            next_field_x = game_field_x + GAME_WIDTH - NEXT_WIDTH
            next_field_y = game_field_y + GAME_HEIGHT + CELL

            # scores
            self.view.draw_text("SCORE",
                                [game_field_x, next_field_y],
                                60, COLOR_WHITE, DEFAULT_FONT, False, False)
            self.view.draw_text(str(self.scores[i]),
                                [game_field_x, next_field_y + 60],
                                60, COLOR_WHITE, DEFAULT_FONT, False, False)

            self.view.draw_grid(next_field_x, next_field_y,
                                NEXT_WIDTH, NEXT_HEIGHT,
                                NEXT_SHAPE_WIDTH, NEXT_SHAPE_HEIGHT)
            self.view.draw_box(next_field_x, next_field_y,
                               NEXT_WIDTH, NEXT_HEIGHT,
                               COLOR_RED, 3)
            for next_x in range(NEXT_SHAPE_WIDTH):
                for next_y in range(NEXT_SHAPE_HEIGHT):
                    if self.game_envs[i].next_shape.at(next_x, next_y) == 1:
                        pygame.draw.rect(self.view.screen, self.game_envs[i].next_shape.color,
                                         pygame.Rect(next_field_x + next_x * CELL, next_field_y + next_y * CELL,
                                                     CELL, CELL))
            if not self.game_envs[i].running:
                pygame.draw.line(self.view.screen, COLOR_RED,
                                 (game_field_x, game_field_y),
                                 (game_field_x + GAME_WIDTH, game_field_y + GAME_HEIGHT), 3)
                pygame.draw.line(self.view.screen, COLOR_RED,
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
        self.view.fill(COLOR_DARK_GRAY)

        self.view.draw_text("TETRIS",
                            [self.view.width // 2, 70],
                            280, COLOR_YELLOW, DEFAULT_FONT, True, False)
        self.view.draw_text("B A T T L E   R O Y A L E",
                            [self.view.width // 2, 250],
                            70, COLOR_RED, DEFAULT_FONT, True, False)

        self.view.draw_text("AGENT-RL",
                            [self.view.width // 2 - 240, 550],
                            60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.view.draw_text("AI: " + self.ai_difficulties[self.ai_rl],
                            [self.view.width // 2 - 240, 600],
                            35, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.view.draw_text("SCORE: " + str(self.scores[0]),
                            [self.view.width // 2 - 240, 640],
                            35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.view.draw_text("|",
                            [self.view.width // 2 - 100, 590],
                            155, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.view.draw_text("PLAYER",
                            [self.view.width // 2, 550],
                            60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.view.draw_text("SCORE: " + str(self.scores[1]),
                            [self.view.width // 2, 600],
                            35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.view.draw_text("PRESS",
                            [self.view.width // 2, 750],
                            60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.view.draw_text("[SPACE]",
                            [self.view.width // 2, 800],
                            35, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.view.draw_text("TO PLAY",
                            [self.view.width // 2, 840],
                            35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.view.draw_text("|",
                            [self.view.width // 2 + 100, 590],
                            155, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.view.draw_text("AGENT-H",
                            [self.view.width // 2 + 240, 550],
                            60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.view.draw_text("AI: " + self.ai_difficulties[self.ai_h],
                            [self.view.width // 2 + 240, 600],
                            35, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.view.draw_text("SCORE: " + str(self.scores[2]),
                            [self.view.width // 2 + 240, 640],
                            35, COLOR_WHITE, DEFAULT_FONT, True, True)

#   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT
