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

        # Przyciski do przejścia do ustawień gry, tabeli wyników oraz wychodzenia z aplikacji

        self.play_button = Button(self.game, pos=(1575, 770), text_var="PLAY", font=self.font, text_color=(255, 255, 255),hover_color=(86, 86, 86),real_screen=self.game.real_screen)
        self.leaderboard_button = Button(self.game, pos=(1575, 885), text_var="LEADERBOARD", font=self.font, text_color=(255, 255, 255),hover_color=(86, 86, 86),real_screen=self.game.real_screen)
        self.close_button = Button(self.game, pos=(1575, 1000), text_var="QUIT", font=self.font, text_color=(255, 255, 255),hover_color=(86, 86, 86),real_screen=self.game.real_screen)

    def update(self, events: list[pygame.event.Event]) -> None:

        # Obsługa najechania na przyciski

        mouse_pos = pygame.mouse.get_pos()
        self.play_button.changeColor(mouse_pos)
        self.leaderboard_button.changeColor(mouse_pos)
        self.close_button.changeColor(mouse_pos)
        for event in events:

            # Obsługa naciśnięcia na przyciski

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkForInput(mouse_pos):
                    self.game.open_settings()

                if self.leaderboard_button.checkForInput(mouse_pos):
                    self.game.show_result()

                if self.close_button.checkForInput(mouse_pos):
                    self.game.running = False


    def draw(self) -> None:
        # Rysowanie wszystkiego na ekranie
        self.game.screen.blit(self.bg,(0,0))
        self.play_button.draw(self.game.screen)
        self.leaderboard_button.draw(self.game.screen)
        self.close_button.draw(self.game.screen)

