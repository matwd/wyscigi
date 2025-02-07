import pygame
import json

class EndScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 40)
        self.name = ""

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif event.key == pygame.K_RETURN:
                    results = []
                    with open("results.json", "r") as file:
                        results = json.load(file)
                    results.append({"name": self.name, "time": self.game.time})
                    with open("results.json", "w") as file:
                        json.dump(results, file)

                    self.name = ""
                    self.game.show_result()
                else:
                    self.name += event.unicode

    def draw(self):
        text_surface, ract = self.font.render(f"{self.name}", pygame.color.THECOLORS["white"], size=0)
        self.game.screen.blit(text_surface, (40, 300))