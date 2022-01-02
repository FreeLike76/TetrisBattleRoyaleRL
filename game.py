import pygame
import numpy


class Game:
    def __init__(self):
        self.game_state = "start"
        self.running = True

    def run(self):
        if self.running:
            if self.game_state == "start":
                pass
            elif self.game_state == "play":
                pass
            elif self.game_state == "end":
                pass
        pygame.quit()