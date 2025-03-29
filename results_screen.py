from __future__ import annotations
import pygame
import json
from button import Button, Cords

class ResultsScreen:
    def __init__(self, game: Game):
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

        self.prev_page_button = Button((self.screen_width // 4 + 20, self.screen_height // 4 + 50 * self.results_per_page + 10 + self.title_text.get_height()), "(<-) PREVIOUS PAGE", self.font, (255, 255, 255), (86, 86, 86), self.game.real_screen, Cords.topleft)
        self.next_page_button = Button((self.screen_width // 4 + self.resultsBg.width - 20, self.screen_height // 4 + 50 * self.results_per_page + 10 + self.title_text.get_height()), "NEXT PAGE (->)", self.font, (255, 255, 255), (86, 86, 86), self.game.real_screen, Cords.topright)

        self.prev_map_button = Button((self.screen_width // 4 + 20, self.screen_height // 4), "<", self.fontBig, (255, 255, 255), (86, 86, 86), self.game.real_screen, Cords.topleft)
        self.next_map_button = Button((self.screen_width // 4 + self.resultsBg.width - 20, self.screen_height // 4), ">", self.fontBig, (255, 255, 255), (86, 86, 86), self.game.real_screen, Cords.topright)

    def update(self, events: list[pygame.event.Event]) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.page == 0:
            self.prev_page_button.changeColor(mouse_pos, True)
        else:
            self.prev_page_button.changeColor(mouse_pos)

        if self.page == self.max_page:
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
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game.selected_map = min(3, self.game.selected_map + 1)
                    self.page = 0
                    self.max_page = -1
                if event.key == pygame.K_DOWN:
                    self.game.selected_map = max(1, self.game.selected_map - 1)
                    self.page = 0
                    self.max_page = -1
                if event.key == pygame.K_LEFT:
                    self.page = max(0, self.page - 1)
                if event.key == pygame.K_RIGHT:
                    self.page = min(self.max_page, self.page + 1)
                if event.key == pygame.K_RETURN:
                    self.game.selected_map = 1
                    self.game.show_main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.prev_page_button.checkForInput(mouse_pos):
                    self.page = max(0, self.page - 1)
                if self.next_page_button.checkForInput(mouse_pos):
                    self.page = min(self.max_page, self.page + 1)
                if self.next_map_button.checkForInput(mouse_pos):
                    self.game.selected_map = min(3, self.game.selected_map + 1)
                    self.page = 0
                    self.max_page = -1
                if self.prev_map_button.checkForInput(mouse_pos):
                    self.game.selected_map = max(1, self.game.selected_map - 1)
                    self.page = 0
                    self.max_page = -1            

    def draw(self) -> None:
        self.game.screen.blit(self.bg, (0, 0))
        pygame.draw.rect(self.game.screen, (0, 0, 0), self.resultsBg)

        results = {
            "map1": [],
            "map2": [],
            "map3": []
        }

        try:
            with open("results.json", "r") as file:
                results = json.load(file)
        except:
            with open("results.json", "w") as file:
                json.dump(results, file)

        ranking = results[f"map{self.game.selected_map}"]

        if self.max_page == -1:
            # przekomiczna imitacja paginacji
            self.max_page = (len(ranking) - 1) // self.results_per_page

        ranking = sorted(ranking, key=lambda x: x["time"])
        
        self.title_text = self.fontBig.render("green map" if self.game.selected_map == 1 else "Petrol City" if self.game.selected_map == 2 else "snow map", True, (255, 255, 255))
        self.game.screen.blit(self.title_text, (self.screen_width // 2 - self.title_text.get_width() // 2, self.screen_height // 4))

        self.prev_map_button.draw(self.game.screen)
        self.next_map_button.draw(self.game.screen)

        for i, result in enumerate(ranking):
            # paginacji ciąg dalszy
            if i < self.page * self.results_per_page:
                continue
            if i >= (self.page + 1) * self.results_per_page:
                break

            nick_surface = self.font.render(f"{result['name']}:", True, (255, 255, 255))
            self.game.screen.blit(nick_surface, (self.screen_width // 4 + 20, self.screen_height // 4 + 50 * (i % self.results_per_page) + self.title_text.get_height() + 10))

            time_surface = self.font.render(f"{float(result['time']):.2f}", True, (255, 255, 255))
            self.game.screen.blit(time_surface, (self.screen_width // 4 + self.resultsBg.width - time_surface.get_width() - 20, self.screen_height // 4 + 50 * (i % self.results_per_page) + self.title_text.get_height() + 10))

        if len(ranking) == 0:
            no_results = self.font.render("No results", True, (255, 255, 255))
            self.game.screen.blit(no_results, (self.screen_width // 2 - no_results.get_width() // 2, self.screen_height // 4 + 50 * self.results_per_page + self.title_text.get_height() + 10))
        else:
            page_text = self.font.render(f"Page {self.page + 1}/{self.max_page + 1}", True, (255, 255, 255))
            self.game.screen.blit(page_text, (self.screen_width // 2 - page_text.get_width() // 2 , self.screen_height // 4 + 50 * self.results_per_page + self.title_text.get_height() + 10))

            self.prev_page_button.draw(self.game.screen)
            self.next_page_button.draw(self.game.screen)


