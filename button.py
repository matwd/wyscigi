from __future__ import annotations
import pygame

class Cords():
    center = 0
    topleft = 1
    topright = 2

class Button():
    """
    Klasa przycisku. Obsługuje najechanie oraz naciśnięcie przycisku
    """
    def __init__(self, game: Game, pos: tuple[int, int], text_var: str, font: pygame.font.Font, text_color: pygame.color.Color, hover_color: pygame.color.Color, real_screen: pygame.surface.Surface, cords: Cords=Cords.center) -> None:
        self.game = game
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.text_color = text_color
        self.hover_color = hover_color
        self.text_var = text_var
        self.real_screen = real_screen
        self.hide = False

        self.text = self.font.render(self.text_var, True, self.text_color)

        # cords to zmienna określająca stosunek położenia buttona do przekazananej pozycji
        if cords == Cords.center:
            self.rect = self.text.get_rect(center=(self.x,self.y))
        elif cords == Cords.topleft:
            self.rect = self.text.get_rect(topleft=(self.x,self.y))
        elif cords == Cords.topright:
            self.rect = self.text.get_rect(topright=(self.x,self.y))

        self.rect.top = self.rect.top + (self.rect.bottom - self.rect.top) / 2
        self.rect.bottom = self.rect.bottom - (self.rect.bottom - self.rect.top) / 2

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.text, self.rect)
        
    def checkForInput(self, position: tuple[int, int]) -> bool:
        """
        Obsługa naciśnięcia przycisku.
        """
        position = [round(position[0]/self.real_screen.get_size()[0] * 1920), round(position[1] / self.real_screen.get_size()[1] * 1080)]
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(int(self.rect.top + (self.rect.bottom - self.rect.top) / 4), int(self.rect.bottom- (self.rect.bottom - self.rect.top) / 5)) and not self.hide:
            if self.game.sound:
                pygame.mixer.Sound("assets/sfx/clickmenu.mp3").play()
            return True
        return False
    
    def changeColor(self, position: tuple[int, int], hide: bool=False) -> None:
        """
        Obsługa zmiany koloru przycisku po najechaniu
        """

        self.hide = hide

        position = [round(position[0]/self.real_screen.get_size()[0] * 1920), round(position[1] / self.real_screen.get_size()[1] * 1080)]
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(int(self.rect.top + (self.rect.bottom - self.rect.top) / 4), int(self.rect.bottom- (self.rect.bottom - self.rect.top) / 5)) and not self.hide:
            # jeżeli najechano na przycisk i nie jest on ukryty, to zmienia kolor na hover_color sprecyzowany w konstruktorze
            self.text = self.font.render(self.text_var, True, self.hover_color)
        elif self.hide:
            # jeżeli przycisk jest ukryty, to wyświetla pusty tekst
            self.text = self.font.render("", True, self.text_color)
        else:
            # jeżeli nie najechano na przycisk i nie jest on ukryrty, to zmienia kolor na text_color sprecyzowany w konstruktorze
            self.text = self.font.render(self.text_var, True, self.text_color)
