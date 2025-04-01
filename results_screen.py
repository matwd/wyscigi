from __future__ import annotations
import pygame
import json
from button import Button, Cords

class ResultsScreen:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.fontBig = pygame.font.Font("assets/font/Jersey10.ttf", 120)
        self.font = pygame.font.Font("assets/font/Jersey10.ttf", 40)
        self.bg = pygame.image.load("assets/menu/mainmenu1920x1080.png").convert()
        self.page = 0
        self.max_page = -1
        self.results_per_page = 7

        self.screen_width = self.game.screen.get_width()
        self.screen_height = self.game.screen.get_height()

        self.resultsBg = pygame.Rect(self.screen_width // 4, self.screen_height // 4, 960, 540)

        self.title_text = self.fontBig.render("Petrol City", True, (255, 255, 255))

        self.prev_page_button = Button(self.game, (self.screen_width // 4 + 20, self.screen_height // 4 + 50 * self.results_per_page + 10 + self.title_text.get_height()), "PREVIOUS PAGE", self.font, (255, 255, 255), (86, 86, 86), self.game.real_screen, Cords.topleft)
        self.next_page_button = Button(self.game, (self.screen_width // 4 + self.resultsBg.width - 20, self.screen_height // 4 + 50 * self.results_per_page + 10 + self.title_text.get_height()), "NEXT PAGE", self.font, (255, 255, 255), (86, 86, 86), self.game.real_screen, Cords.topright)

        self.prev_map_button = Button(self.game, (self.screen_width // 4 + 20, self.screen_height // 4), "<", self.fontBig, (255, 255, 255), (86, 86, 86), self.game.real_screen, Cords.topleft)
        self.next_map_button = Button(self.game, (self.screen_width // 4 + self.resultsBg.width - 20, self.screen_height // 4), ">", self.fontBig, (255, 255, 255), (86, 86, 86), self.game.real_screen, Cords.topright)

        self.close_button = Button(self.game, (self.screen_width // 4 + 10, self.screen_height // 4), "X", self.font, (255, 255, 255), (255, 0, 0), self.game.real_screen, Cords.topleft)
        self.selected_map = 1
        self.ranking = []
        self.load_map(1)
    
    def next_map(self) -> None:
        self.game.selected_map = min(3, self.game.selected_map + 1)
        self.page = 0
        self.max_page = -1
        self.load_map(self.game.selected_map)

    def prev_map(self) -> None:
        self.game.selected_map = max(1, self.game.selected_map - 1)
        self.page = 0
        self.max_page = -1
        self.load_map(self.game.selected_map)

    def next_page(self) -> None:
        self.page = min(self.max_page, self.page + 1)

    def prev_page(self) -> None:
        self.page = max(0, self.page - 1)

    def load_map(self, map: int):
        self.selected_map = map
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

        # wybieramy ranking dla wybranej mapy
        self.ranking = results[f"map{map}"]

        if self.max_page == -1:
            # przekomiczna imitacja paginacji
            self.max_page = (len(self.ranking) - 1) // self.results_per_page

        # sortowanie wyników po czasie
        self.ranking = list(sorted(self.ranking, key=lambda x: x["time"]))

    def update(self, events: list[pygame.event.Event]) -> None:
        mouse_pos = pygame.mouse.get_pos()

        # jeśli któryś guzik powinien być nieaktywny, to jest ukrywanym, w przeciwnym wypadku sprawdzamy czy jest hover i jeśli tak to zmieniamy kolor
        if self.page == 0:
            self.prev_page_button.changeColor(mouse_pos, True)
        else:
            self.prev_page_button.changeColor(mouse_pos)

        if self.page == self.max_page or self.max_page == -1:
            self.next_page_button.changeColor(mouse_pos, True)
        else:
            self.next_page_button.changeColor(mouse_pos)

        if self.game.selected_map == 1:
            self.prev_map_button.changeColor(mouse_pos, True)
        else:
            self.prev_map_button.changeColor(mouse_pos)

        if self.game.selected_map == 3:
            self.next_map_button.changeColor(mouse_pos, True)
        else:
            self.next_map_button.changeColor(mouse_pos)
        self.close_button.changeColor(mouse_pos)    

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.prev_page()
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.next_page()
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.next_map()
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.prev_map()
                if event.key == pygame.K_RETURN:
                    self.game.selected_map = 1
                    self.game.show_main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.close_button.checkForInput(mouse_pos):
                    self.game.show_main()
                if self.next_map_button.checkForInput(mouse_pos):
                    self.next_map()
                if self.prev_map_button.checkForInput(mouse_pos):
                    self.prev_map()
                if self.next_page_button.checkForInput(mouse_pos):
                    self.next_page()
                if self.prev_page_button.checkForInput(mouse_pos):
                    self.prev_page()

    def draw(self) -> None:
        self.game.screen.blit(self.bg, (0, 0))
        pygame.draw.rect(self.game.screen, (0, 0, 0), self.resultsBg)

        # wyświetlanie nazwy mapy
        self.title_text = self.fontBig.render("Countryside Circuit" if self.game.selected_map == 1 else "Petrol City" if self.game.selected_map == 2 else "Snowy Slipstream", True, (255, 255, 255))
        self.game.screen.blit(self.title_text, (self.screen_width // 2 - self.title_text.get_width() // 2, self.screen_height // 4))

        self.prev_map_button.draw(self.game.screen)
        self.next_map_button.draw(self.game.screen)
        self.close_button.draw(self.game.screen)

        for i, result in enumerate(self.ranking):
            # paginacji ciąg dalszy
            if i < self.page * self.results_per_page:
                continue
            if i >= (self.page + 1) * self.results_per_page:
                break

            # wyświetlanie nazwy gracza
            nick_surface = self.font.render(f"{result['name']}:", True, (255, 255, 255))
            self.game.screen.blit(nick_surface, (self.screen_width // 4 + 20, self.screen_height // 4 + 50 * (i % self.results_per_page) + self.title_text.get_height() + 10))

            # wyświetlanie zajętego miejsca
            time_surface = self.font.render(str(result['rank']), True, (255, 255, 255))
            self.game.screen.blit(time_surface, (self.screen_width // 4 + self.resultsBg.width - time_surface.get_width() - 120, self.screen_height // 4 + 50 * (i % self.results_per_page) + self.title_text.get_height() + 10))

            # wyświetlanie czasu
            time_surface = self.font.render(f"{float(result['time']):.2f}", True, (255, 255, 255))
            self.game.screen.blit(time_surface, (self.screen_width // 4 + self.resultsBg.width - time_surface.get_width() - 20, self.screen_height // 4 + 50 * (i % self.results_per_page) + self.title_text.get_height() + 10))

        if len(self.ranking) == 0:
            # jeśli nie ma wyników to wyświetlamy stosowny komunikat
            no_results = self.font.render("No results", True, (255, 255, 255))
            self.game.screen.blit(no_results, (self.screen_width // 2 - no_results.get_width() // 2, self.screen_height // 4 + 50 * self.results_per_page + self.title_text.get_height() + 10))
        else:
            # wyświetlanie informacji o stronie
            page_text = self.font.render(f"Page {self.page + 1}/{self.max_page + 1}", True, (255, 255, 255))
            self.game.screen.blit(page_text, (self.screen_width // 2 - page_text.get_width() // 2 , self.screen_height // 4 + 50 * self.results_per_page + self.title_text.get_height() + 10))

            self.prev_page_button.draw(self.game.screen)
            self.next_page_button.draw(self.game.screen)


