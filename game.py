import pygame
import numpy


class Game:
    def __init__(self):
        self.game_state = "start"
        self.running = True

    def run(self):
        if self.running:
            if self.game_state == "start":
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.game_state == "play":
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.game_state == "end":
                self.start_events()
                self.start_update()
                self.start_draw()
        pygame.quit()

#   START   START   START   START   START   START   START   START   START   START   START

    def start_events(self):
        pass

    def start_update(self):
        pass

    def start_draw(self):
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
    def draw_text(self):
        pass