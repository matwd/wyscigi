import pygame
from button import Button


class GameSettings:
    def __init__(self, game):

        self.game = game
        self.font = pygame.font.Font("assets/font/8-BIT WONDER.TTF", 100)
        self.play_button = Button(pos=(960, 930), text_var="START THE RACE", font=self.font, text_color=(255,255,255),
                                  hover_color=(86,86,86),real_screen=self.game.real_screen) #dodac flage szachownice do tła
        self.car_pick_text = self.font.render("CHOOSE YOUR CAR", True, (255,255,255))
        self.car_pick_rect = self.car_pick_text.get_rect(center=(960, 150))

        self.car_1_btn = Button(pos=(384,350),text_var="CAR 1", font=self.font, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)
        self.car_2_btn = Button(pos=(768,350),text_var="CAR 2", font=self.font, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)
        self.car_3_btn = Button(pos=(1152,350),text_var="CAR 3", font=self.font, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)
        self.car_4_btn = Button(pos=(1536,350),text_var="CAR 4", font=self.font, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)

        self.car_btns = [self.car_1_btn,self.car_2_btn,self.car_3_btn,self.car_4_btn]

        self.chosen_car = 1

        self.map_pick_text = self.font.render("CHOOSE THE MAP", True, (255,255,255))
        self.map_pick_rect = self.map_pick_text.get_rect(center=(960, 550))

        self.map_1_btn = Button(pos=(480,700),text_var="MAP 1", font=self.font, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)
        self.map_2_btn = Button(pos=(960,700),text_var="MAP 2", font=self.font, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)
        self.map_3_btn = Button(pos=(1440,700),text_var="MAP 3", font=self.font, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)

        self.chosen_map = 1

        self.map_btns = [self.map_1_btn,self.map_2_btn,self.map_3_btn]


    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.play_button.changeColor(mouse_pos)

        for index, car_btn in enumerate(self.car_btns,start=1):
            car_btn.text_color=(255,255,255)
            if index == self.chosen_car:
                car_btn.text_color = (86,86,86)
            car_btn.changeColor(mouse_pos)
            
                
        for index, map_btn in enumerate(self.map_btns,start=1):
            map_btn.text_color = (255,255,255)
            if index == self.chosen_map:
                map_btn.text_color=(86,86,86)
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
