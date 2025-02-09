import pygame
from button import Button

class MainMenu:
    def __init__(self, game):
        
        self.game = game
        self.font = pygame.font.SysFont(None, 40)
        self.play_button = Button(pos=(200,300), text_var="GRAJ", font=self.font, text_color=(255, 0, 0),hover_color=(255, 141, 161))

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.play_button.changeColor(mouse_pos)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkForInput(mouse_pos):
                    self.game.start_race(0, 0)


    def draw(self):
        self.play_button.update(self.game.screen)
