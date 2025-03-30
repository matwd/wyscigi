from __future__ import annotations
import pygame
import json

class EndScreen:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.font = pygame.font.Font("assets/font/Jersey10.ttf", 40)
        self.bg = pygame.image.load("assets/menu/mainmenu1920x1080.png").convert()
        self.name = ""

        self.screen_width = self.game.screen.get_width()
        self.screen_height = self.game.screen.get_height()

        self.smallerBg = pygame.Rect(self.screen_width // 4, self.screen_height // 4, 960, 540)

    def update(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # usuwa ostatni znak jeśli klinie się backspace
                    self.name = self.name[:-1]
                elif event.key == pygame.K_RETURN:
                    # sprawdza czy nazwa nie jest pusta i jeśli nie jest to zapisuje wynik do pliku
                    if self.name == "":
                        return

                    results = {
                        "map1": [],
                        "map2": [],
                        "map3": []
                    }

                    try:
                        with open("results.json", "r") as file:
                            results = json.load(file)
                    except:
                        # jeśli nie ma pliku to go tworzy z pustymi arrayem json
                        with open("results.json", "w") as file:
                            json.dump(results, file)

                    results[f"map{self.game.selected_map}"].append(
                        {"name": self.name,
                         "time": float(self.game.ms_to_sec(self.game.time)),
                         "rank": self.game.player_rank})

                    with open("results.json", "w") as file:
                        json.dump(results, file)

                    self.name = ""
                    self.game.show_result()
                elif len(self.name) < 32:
                    self.name += event.unicode

    def draw(self) -> None:
        # draws background and black rectangle in the middle of the screen
        self.game.screen.blit(self.bg, (0, 0))
        pygame.draw.rect(self.game.screen, (0, 0, 0), self.smallerBg)

        # draws text with rank
        rank_surface = self.font.render(f"Your rank: {self.game.player_rank}", True, (255, 255, 255))
        self.game.screen.blit(rank_surface, (self.screen_width // 2 - rank_surface.get_width() // 2, self.screen_height // 4))

        # draws text with time
        time_surface = self.font.render(f"Your time: {self.game.ms_to_sec(self.game.time)}s", True, (255, 255, 255))
        self.game.screen.blit(time_surface, (self.screen_width // 2 - time_surface.get_width() // 2, self.screen_height // 4 + 50))

        # draws text with prompt to enter name
        enter_name_surface = self.font.render("Enter your name:", True, (255, 255, 255))
        self.game.screen.blit(enter_name_surface, (self.screen_width // 2 - enter_name_surface.get_width() // 2, self.screen_height // 4 + 100))

        # draws text with name
        name_surface = self.font.render(self.name, True, (255, 255, 255))
        self.game.screen.blit(name_surface, (self.screen_width // 2 - name_surface.get_width() // 2, self.screen_height // 4 + 150))

