import pygame
import numpy
from settings import *
from game_env.game_env import GameEnv

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.game_state = "start"
        self.running = True

    def run(self):
        if self.running:
            if self.game_state == "start":
                self.start_events()
                self.start_update()
                self.start_draw()

            if self.game_state == "load":
                self.load_draw()
                self.load_update()

            elif self.game_state == "play":
                self.start_events()
                self.start_update()
                self.start_draw()

            elif self.game_state == "end":
                self.start_events()
                self.start_update()
                self.start_draw()

            # update screen

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
        self.screen.fill((0, 0, 0))

        # menu
        self.draw_text("TETRIS BATTLE ROYALE",
                       [SCREEN_WIDTH // 2, SCREEN_HEIGHT],
                       20, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.draw_text("Dmytro Geleshko",
                       [SCREEN_WIDTH // 2, SCREEN_HEIGHT + 20],
                       12, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.draw_text("IP-91",
                       [SCREEN_WIDTH // 2, SCREEN_HEIGHT + 40],
                       12, COLOR_WHITE, DEFAULT_FONT, True, True)
        self.draw_text("PRESS SPACE TO PLAY",
                       [SCREEN_WIDTH // 2, SCREEN_HEIGHT + 60],
                       16, COLOR_WHITE, DEFAULT_FONT, True, True)

#   LOAD    LOAD   LOAD    LOAD   LOAD    LOAD   LOAD    LOAD   LOAD    LOAD   LOAD    LOAD

    def load_draw(self):
        pass

    def load_update(self):
        pass

#   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY  PLAY   PLAY

    def play_events(self):
        pass

    def play_update(self):
        pass

    def play_draw(self):
        pass

#   END   END   END   END   END   END   END   END   END   END   END   END   END   END

    def end_events(self):
        pass

    def end_update(self):
        pass

    def end_draw(self):
        pass

#   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT   SUPPORT

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
