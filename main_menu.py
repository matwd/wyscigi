import pygame

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 40)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.game.state = 1
                self.game.gameState = 1

    def draw(self):
        text_surface, ract = self.font.render("Kliknij dowolny klawisz aby zacząć", pygame.color.THECOLORS["white"], size=0)
        self.game.screen.blit(text_surface, (40, 300))
