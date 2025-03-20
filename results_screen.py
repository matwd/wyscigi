import pygame
import json

class ResultsScreen:
    def __init__(self, game):
        self.game = game
        self.fontBig = pygame.font.Font("assets/font/8-BIT WONDER.TTF", 100)
        self.font = pygame.font.Font("assets/font/8-BIT_WONDER.ttf", 40)
        self.page = 0
        self.max_page = -1

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.page = max(0, self.page - 1)
                if event.key == pygame.K_n:
                    self.page = min(self.max_page, self.page + 1)
                if event.key == pygame.K_RETURN:
                    self.game.show_main()

    def draw(self):
        ranking = []

        with open("results.json", "r") as file:
            ranking = json.load(file)

        if self.max_page == -1:
            # przekomiczna imitacja paginacji
            self.max_page = len(ranking) // 8

        ranking = sorted(ranking, key=lambda x: x["time"])
        
        test_surface = self.fontBig.render("Results", True, (255, 255, 255))
        self.game.screen.blit(test_surface, (40, 40))

        for i, result in enumerate(ranking):
            # paginacji ciąg dalszy
            if i < self.page * 8:
                continue
            if i >= (self.page + 1) * 8:
                break

            text_surface = self.font.render(f"{result['name']}: {float(result['time']):.2f}", True, (255, 255, 255))
            self.game.screen.blit(text_surface, (40, 200 + i * 40))
