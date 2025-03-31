from __future__ import annotations
import pygame
from button import Button

class MainMenu:
    """
    Klasa odpowiedzialna za menu główne gry
    """
    def __init__(self, game: Game) -> None:
        self.game = game
        self.font = pygame.font.Font("assets/font/Jersey10.ttf", 140)
        self.bg = pygame.image.load("assets/menu/mainmenu1920x1080.png").convert()

        self.bg = pygame.transform.scale(self.bg,[1920,1080])
        self.play_button = Button(pos=(1575, 775), text_var="PLAY", font=self.font, text_color=(255, 255, 255),hover_color=(86, 86, 86),real_screen=self.game.real_screen)
        self.leaderboard_button = Button(pos=(1575, 925), text_var="LEADERBOARD", font=self.font, text_color=(255, 255, 255),hover_color=(86, 86, 86),real_screen=self.game.real_screen)

    def update(self, events: list[pygame.event.Event]) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.play_button.changeColor(mouse_pos)
        self.leaderboard_button.changeColor(mouse_pos)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkForInput(mouse_pos):
                    self.game.open_settings()

                if self.leaderboard_button.checkForInput(mouse_pos):
                    self.game.show_result()


    def draw(self) -> None:
        self.game.screen.blit(self.bg,(0,0))
        self.play_button.draw(self.game.screen)
        self.leaderboard_button.draw(self.game.screen)

