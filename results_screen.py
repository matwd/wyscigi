import pygame
import json

class ResultsScreen:
    def __init__(self, game):
        self.game = game
        self.fontBig = pygame.font.Font("assets/font/Jersey10.ttf", 120)
        self.font = pygame.font.Font("assets/font/Jersey10.ttf", 40)
        self.bg = pygame.image.load("assets/menu/mainmenu1920x1080.png").convert()
        self.page = 0
        self.max_page = -1

        self.screen_width = self.game.screen.get_width()
        self.screen_height = self.game.screen.get_height()

        self.resultsBg = pygame.Rect(self.screen_width // 4, self.screen_height // 4, 960, 540)

    def update(self, events):
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
                if event.key == pygame.K_p:
                    self.page = max(0, self.page - 1)
                if event.key == pygame.K_n:
                    self.page = min(self.max_page, self.page + 1)
                if event.key == pygame.K_RETURN:
                    self.game.selected_map = 1
                    self.game.show_main()

    def draw(self):
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
            with open("results.json", "r") as file:
                json.dump(results, file)

        ranking = results[f"map{self.game.selected_map}"]

        if self.max_page == -1:
            # przekomiczna imitacja paginacji
            self.max_page = len(ranking) // 8

        ranking = sorted(ranking, key=lambda x: x["time"])
        
        title_text = self.fontBig.render(f"Results (map {self.game.selected_map})", True, (255, 255, 255))
        self.game.screen.blit(title_text, (self.screen_width // 2 - title_text.get_width() // 2, self.screen_height // 4))

        for i, result in enumerate(ranking):
            # paginacji ciąg dalszy
            if i < self.page * 8:
                continue
            if i >= (self.page + 1) * 8:
                break

            nick_surface = self.font.render(f"{result['name']}:", True, (255, 255, 255))
            self.game.screen.blit(nick_surface, (self.screen_width // 4 + 20, self.screen_height // 4 + 50 * (i % 8) + title_text.get_height() + 10))

            time_surface = self.font.render(f"{float(result['time']):.2f}", True, (255, 255, 255))
            self.game.screen.blit(time_surface, (self.screen_width // 4 + self.resultsBg.width - time_surface.get_width() - 20, self.screen_height // 4 + 50 * (i % 8) + title_text.get_height() + 10))

