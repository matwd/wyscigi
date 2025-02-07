import pygame
import json

class ResultsScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 40)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.show_main()

    def draw(self):
        ranking = []

        with open("results.json", "r") as file:
            ranking = json.load(file)
        
        for i, result in enumerate(ranking):
            if i > 7:
                break

            text_surface, ract = self.font.render(f"{result['name']}: {float(result['time']):.2f}", pygame.color.THECOLORS["white"], size=0)
            self.game.screen.blit(text_surface, (40, 40 + (50 * i)))