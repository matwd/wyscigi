import pygame
from button import Button
from car import PlayerCar

class CountdownScreen:
    """
    Klasa odpowiedzialna za ekran z odliczaniem do rozpoczęcia
    """
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("assets/font/Jersey10.ttf", 1000)
        self.last_frame_time = pygame.time.get_ticks()
        self.time = 4

        self.time_text = self.font.render(str(self.time), True, (255,255,255))
        self.time_text_rect = self.time_text.get_rect(center=(960, 540))

    def update(self, events):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > 1000:
            self.time-=1
            if self.time == 0:
                self.game.start_race()
                self.time = 4
            self.time_text = self.font.render(str(self.time), True, (255,255,255))
            self.last_frame_time = current_time


    def draw(self):
        self.game.draw_everything()
        if self.time != 4:
            self.game.screen.blit(self.time_text, self.time_text_rect)

