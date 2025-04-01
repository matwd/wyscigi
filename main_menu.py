from __future__ import annotations
import pygame
from button import Button, Cords

class MainMenu:
    """
    Klasa odpowiedzialna za menu główne gry
    """
    def __init__(self, game: Game) -> None:
        self.game = game
        self.font = pygame.font.Font("assets/font/Jersey10.ttf", 140)
        self.iconFont = pygame.font.Font("assets/font/soundicon.ttf", 100)
        self.bg = pygame.image.load("assets/menu/mainmenu1920x1080.png").convert()
        self.bg = pygame.transform.scale(self.bg,[1920,1080])

        # Przyciski do przejścia do ustawień gry, tabeli wyników oraz wychodzenia z aplikacji

        self.play_button = Button(self.game, pos=(1575, 770), text_var="PLAY", font=self.font, text_color=(255, 255, 255),hover_color=(86, 86, 86),real_screen=self.game.real_screen)
        self.leaderboard_button = Button(self.game, pos=(1575, 885), text_var="LEADERBOARD", font=self.font, text_color=(255, 255, 255),hover_color=(86, 86, 86),real_screen=self.game.real_screen)
        self.close_button = Button(self.game, pos=(1575, 1000), text_var="QUIT", font=self.font, text_color=(255, 255, 255),hover_color=(86, 86, 86),real_screen=self.game.real_screen)

        # Przycisk do wyciszenia dźwięku
        # Stworzyliśmy do niego specjalną czcionkę, która zawiera ikonki głośnika, 'B' - dzięk włączony, 'C' - dźwięk wyłączony
        self.mute_button = Button(self.game, pos=(20, 0), text_var="B", font=self.iconFont, text_color=(255, 255, 255),hover_color=(86, 86, 86),real_screen=self.game.real_screen, cords=Cords.topleft)

    def update(self, events: list[pygame.event.Event]) -> None:

        # Obsługa najechania na przyciski

        mouse_pos = pygame.mouse.get_pos()
        self.play_button.changeColor(mouse_pos)
        self.leaderboard_button.changeColor(mouse_pos)
        self.close_button.changeColor(mouse_pos)

        if self.game.speakers:
            self.mute_button.changeColor(mouse_pos)
            self.mute_button.text_var = "B" if self.game.sound else "C"

        for event in events:

            # Obsługa naciśnięcia na przyciski

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkForInput(mouse_pos):
                    self.game.open_settings()

                if self.leaderboard_button.checkForInput(mouse_pos):
                    self.game.show_result()

                if self.close_button.checkForInput(mouse_pos):
                    self.game.running = False

                if self.mute_button.checkForInput(mouse_pos) and self.game.speakers:
                    if self.game.sound:
                        self.game.sound = False
                        self.game.music.set_volume(0)
                    else:
                        self.game.sound = True
                        self.game.music.set_volume(1)


    def draw(self) -> None:
        # Rysowanie wszystkiego na ekranie
        self.game.screen.blit(self.bg,(0,0))
        self.play_button.draw(self.game.screen)
        self.leaderboard_button.draw(self.game.screen)
        self.close_button.draw(self.game.screen)

        if self.game.speakers:
            self.mute_button.draw(self.game.screen)

