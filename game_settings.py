import pygame
from button import Button


class GameSettings:
    def __init__(self, game):

        self.game = game
        self.font = pygame.font.SysFont(None, 40)
        self.play_button = Button(pos=(200, 300), text_var="ROZPOCZNIJ WYŚCIG", font=self.font, text_color=(255, 0, 0),
                                  hover_color=(255, 141, 161)) #dodac flage szachownice do tła
        self.car_pick_text = self.font.render("Wybierz swoje auto", True, (255, 0, 0))
        self.car_pick_rect = self.car_pick_text.get_rect(center=(300, 100))

        self.map_pick_text = self.font.render("Wybierz mapę", True, (255, 0, 0))
        self.map_pick_rect = self.map_pick_text.get_rect(center=(300, 150))


    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.play_button.changeColor(mouse_pos)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkForInput(mouse_pos):
                    self.game.start_race(0, 0)

    def draw(self):
        self.play_button.update(self.game.screen)
        self.game.screen.blit(self.map_pick_text, self.map_pick_rect)
        self.game.screen.blit(self.car_pick_text, self.car_pick_rect)
