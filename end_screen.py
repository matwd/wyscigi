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
                    # usuwa ostatni znak jeśli klinie się backspace
                    self.name = self.name[:-1]
                elif event.key == pygame.K_RETURN:
                    # sprawdza czy nazwa nie jest pusta i jeśli nie jest to zapisuje wynik do pliku
                    if self.name == "":
                        return

                    results = []

                    try:
                        with open("results.json", "r") as file:
                            results = json.load(file)
                    except:
                        # jeśli nie ma pliku to go tworzy z pustym arrayem json
                        with open("results.json", "w") as file:
                            file.write("[]")

                    results.append({"name": self.name, "time": float(self.game.ms_to_sec(self.game.time))})
                    with open("results.json", "w") as file:
                        json.dump(results, file)

                    self.name = ""
                    self.game.show_result()
                else:
                    self.name += event.unicode

    def draw(self):
        text_surface, ract = self.font.render(f"ur time: {self.game.ms_to_sec(self.game.time)}", pygame.color.THECOLORS["white"], size=0)
        self.game.screen.blit(text_surface, ((self.game.screen.get_width() / 2) - ract.width / 2, 200))

        text_surface, ract = self.font.render(f"{self.name}", pygame.color.THECOLORS["white"], size=0)
        self.game.screen.blit(text_surface, ((self.game.screen.get_width() / 2) - ract.width / 2, 300))

