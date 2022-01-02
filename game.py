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
        self.play_inputs = None

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
                self.start_events()
                self.start_update()
                self.start_draw()

            elif self.game_state == "end":
                self.start_events()
                self.start_update()
                self.start_draw()

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
                    self.game_state = "load_play"
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
        self.screen.fill((50, 50, 50))

        self.draw_text("TETRIS",
                       [DISPLAY_WIDTH // 2, 0],
                       280, COLOR_YELLOW, DEFAULT_FONT, True, False)
        self.draw_text("B A T T L E   R O Y A L E",
                       [DISPLAY_WIDTH // 2, 180],
                       70, COLOR_RED, DEFAULT_FONT, True, False)

        self.draw_text("AGENT L",
                       [DISPLAY_WIDTH // 2 - 240, 375],
                       60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.draw_text("AI: " + self.ai_difficulties[self.ai_l],
                       [DISPLAY_WIDTH // 2 - 240, 425],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.draw_text("[A] TO CHANGE",
                       [DISPLAY_WIDTH // 2 - 240, 465],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("|",
                       [DISPLAY_WIDTH // 2 - 100, 390],
                       155, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("PLAY",
                       [DISPLAY_WIDTH // 2, 350],
                       60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.draw_text("[SPACE]",
                       [DISPLAY_WIDTH // 2, 410],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("|",
                       [DISPLAY_WIDTH // 2 + 100, 390],
                       155, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("AGENT R",
                       [DISPLAY_WIDTH // 2 + 240, 375],
                       60, COLOR_YELLOW, DEFAULT_FONT, True, True)
        self.draw_text("AI: " + self.ai_difficulties[self.ai_r],
                       [DISPLAY_WIDTH // 2 + 240, 425],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.draw_text("[D] TO CHANGE",
                       [DISPLAY_WIDTH // 2 + 240, 465],
                       35, COLOR_WHITE, DEFAULT_FONT, True, True)

        self.draw_text("By Dmytro Geleshko",
                       [40, 600],
                       30, COLOR_WHITE, DEFAULT_FONT, False, False)


#   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD

    def play_load_draw(self):
        pass

    def play_load_update(self):
        self.env = GameEnv()
        pass

#   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY   PLAY   PLAY

    def play_events(self):
        pass

    def play_update(self):
        pass

    def play_draw(self):
        pass

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
