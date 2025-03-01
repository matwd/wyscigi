import pygame

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("./assets/6809 Chargen.otf", 40)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.game.start_race(0, 0)

    def draw(self):
        text_surface = self.font.render("Kliknij dowolny klawisz aby zacząć", True, pygame.color.THECOLORS["white"])
        self.game.screen.blit(text_surface, (40, 300))
