import pygame

class Button():
    """
    Klasa przycisku. Obsługuje najechanie oraz naciśnięcie przycisku
    """
    def __init__(self, pos: tuple[int, int], text_var: str, font: pygame.font.Font, text_color: pygame.color.Color, hover_color: pygame.color.Color, real_screen: pygame.surface.Surface) -> None:
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.text_color = text_color
        self.hover_color = hover_color
        self.text_var = text_var
        self.real_screen = real_screen
        self.text = self.font.render(self.text_var, True, self.text_color)
        self.rect = self.text.get_rect(center=(self.x,self.y))

    def update(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.text, self.rect)
        
    def checkForInput(self, position: tuple[int, int]) -> bool:
        """
        Obsługa naciśnięcia przycisku.
        """
        position = [round(position[0]/self.real_screen.get_size()[0] * 1920), round(position[1] / self.real_screen.get_size()[1] * 1080)]
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position: tuple[int, int]) -> None:
        """
        Obsługa zmiany koloru przycisku po najechaniu
        """
        position = [round(position[0]/self.real_screen.get_size()[0] * 1920), round(position[1] / self.real_screen.get_size()[1] * 1080)]
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_var,True,self.hover_color)
        else:
            self.text = self.font.render(self.text_var, True, self.text_color)