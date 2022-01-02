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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game_state = "load"

    def start_update(self):
        # for player: choose action or None
        # for game_env: apply action
        pass

    def start_draw(self):
        # fill background
        self.screen.fill((50, 50, 50))

        self.draw_text("TETRIS",
                       [DISPLAY_WIDTH // 2, -20],
                       200, COLOR_YELLOW, DEFAULT_FONT, True, False)
        self.draw_text("B A T T L E   R O Y A L E",
                       [DISPLAY_WIDTH // 2, 180],
                       70, COLOR_RED, DEFAULT_FONT, True, False)

        self.draw_text("| PLAY",
                       [40, 320],
                       60, COLOR_WHITE, DEFAULT_FONT, False, False)
        self.draw_text("| AGENT L",
                       [40, 380],
                       60, COLOR_WHITE, DEFAULT_FONT, False, False)
        self.draw_text("med",
                       [275, 385],
                       25, COLOR_WHITE, DEFAULT_FONT, False, False)
        self.draw_text("[ L ] to change",
                       [275, 415],
                       25, COLOR_WHITE, DEFAULT_FONT, False, False)
        self.draw_text("| AGENT R",
                       [40, 440],
                       60, COLOR_WHITE, DEFAULT_FONT, False, False)
        self.draw_text("med",
                       [275, 445],
                       25, COLOR_WHITE, DEFAULT_FONT, False, False)
        self.draw_text("[ R ] to change",
                       [275, 475],
                       25, COLOR_WHITE, DEFAULT_FONT, False, False)

        self.draw_text("By Dmytro Geleshko",
                       [40, 600],
                       30, COLOR_WHITE, DEFAULT_FONT, False, False)


#   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD   PLAY LOAD    PLAY LOAD

    def play_load_draw(self):
        pass

    def play_load_update(self):
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
