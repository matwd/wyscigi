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

        self.car_1_btn = Button(pos=(200,125),text_var="Auto 1", font=self.font, text_color=(255,0,0),hover_color=(255,141,161))
        self.car_2_btn = Button(pos=(300,125),text_var="Auto 2", font=self.font, text_color=(255,0,0),hover_color=(255,141,161))
        self.car_3_btn = Button(pos=(400,125),text_var="Auto 3", font=self.font, text_color=(255,0,0),hover_color=(255,141,161))
        self.car_4_btn = Button(pos=(500,125),text_var="Auto 4", font=self.font, text_color=(255,0,0),hover_color=(255,141,161))

        self.car_btns = [self.car_1_btn,self.car_2_btn,self.car_3_btn,self.car_4_btn]

        self.chosen_car = 1

        self.map_pick_text = self.font.render("Wybierz mapę", True, (255, 0, 0))
        self.map_pick_rect = self.map_pick_text.get_rect(center=(300, 150))

        self.map_1_btn = Button(pos=(200,175),text_var="Mapa 1", font=self.font, text_color=(255,0,0),hover_color=(255,141,161))
        self.map_2_btn = Button(pos=(300,175),text_var="Mapa 2", font=self.font, text_color=(255,0,0),hover_color=(255,141,161))
        self.map_3_btn = Button(pos=(400,175),text_var="Mapa 3", font=self.font, text_color=(255,0,0),hover_color=(255,141,161))

        self.chosen_map = 1

        self.map_btns = [self.map_1_btn,self.map_2_btn,self.map_3_btn]


    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.play_button.changeColor(mouse_pos)
        self.car_1_btn.changeColor(mouse_pos)
        self.car_2_btn.changeColor(mouse_pos)
        self.car_3_btn.changeColor(mouse_pos)
        self.car_4_btn.changeColor(mouse_pos)

        for car_btn in self.car_btns:
            car_btn.changeColor(mouse_pos)
                
        for map_btn in self.map_btns:
            map_btn.changeColor(mouse_pos)
            

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkForInput(mouse_pos):
                    print("Wybrane auto:",self.chosen_car)
                    print("Wybrana mapa:",self.chosen_map)
                    self.game.start_race(0, 0)
                for index, car_btn in enumerate(self.car_btns,start=1):
                    if car_btn.checkForInput(mouse_pos):
                        self.chosen_car=index
                
                for index, map_btn in enumerate(self.map_btns,start=1):
                    if map_btn.checkForInput(mouse_pos):
                        self.chosen_map=index
                

    def draw(self):
        self.play_button.update(self.game.screen)
        for car_btn in self.car_btns:
            car_btn.update(self.game.screen)
        for map_btn in self.map_btns:
            map_btn.update(self.game.screen)
        self.game.screen.blit(self.map_pick_text, self.map_pick_rect)
        self.game.screen.blit(self.car_pick_text, self.car_pick_rect)
