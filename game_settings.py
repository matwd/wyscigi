from __future__ import annotations
import pygame
from button import Button


class GameSettings:
    """
    Klasa odpowiedzialna za ekran z wyborem pojazdu oraz mapy  
    """
    def __init__(self, game: Game) -> None:

        self.car_frame_index = 6
        self.last_frame_time = pygame.time.get_ticks()

        self.game = game
        self.font_large = pygame.font.Font("assets/font/Jersey10.ttf", 100)
        self.font_normal = pygame.font.Font("assets/font/Jersey10.ttf", 50)

        # Obrazki aut oraz ich lista

        self.car_sprites = [
            [pygame.image.load(f"assets/car-sprites/car-01/{i:>04}.png") for i in range(1, 17)],
            [pygame.image.load(f"assets/car-sprites/car-02/{i:>04}.png") for i in range(1, 17)],
            [pygame.image.load(f"assets/car-sprites/car-03/{i:>04}.png") for i in range(1, 17)],
            [pygame.image.load(f"assets/car-sprites/car-04/{i:>04}.png") for i in range(1, 17)],
            [pygame.image.load(f"assets/car-sprites/car-05/{i:>04}.png") for i in range(1, 17)]
        ]

        self.car_1_img = pygame.transform.scale(self.car_sprites[0][6],[300,300])
        self.car_2_img = pygame.transform.scale(self.car_sprites[1][6],[300,300])
        self.car_3_img = pygame.transform.scale(self.car_sprites[2][6],[300,300])
        self.car_4_img = pygame.transform.scale(self.car_sprites[3][6],[300,300])
        self.car_5_img = pygame.transform.scale(self.car_sprites[4][6],[300,300])

        self.car_imgs = [self.car_1_img,self.car_2_img,self.car_3_img,self.car_4_img,self.car_5_img]

        # Obrazki map oraz ich lista

        self.map_1_img = pygame.transform.scale(pygame.image.load("assets/menu_miniatures/map1.png"),[400,225])
        self.map_2_img = pygame.transform.scale(pygame.image.load("assets/menu_miniatures/map2.png"),[400,225])
        self.map_3_img = pygame.transform.scale(pygame.image.load("assets/menu_miniatures/map3.png"),[400,225])

        self.map_imgs = [self.map_1_img,self.map_2_img,self.map_3_img]

        # Przyciski do wyboru pojazdu
        
        self.car_pick_text = self.font_large.render("CHOOSE YOUR CAR", True, (255,255,255))
        self.car_pick_rect = self.car_pick_text.get_rect(center=(960, 100))

        self.car_1_btn = Button(pos=(320,470),text_var="Orange Overtaker", font=self.font_normal, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)
        self.car_2_btn = Button(pos=(640,470),text_var="Cobalt Crusher", font=self.font_normal, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)
        self.car_3_btn = Button(pos=(960,470),text_var="Crimson Conqueror", font=self.font_normal, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)
        self.car_4_btn = Button(pos=(1280,470),text_var="Verdant Vandal", font=self.font_normal, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)
        self.car_5_btn = Button(pos=(1600,470),text_var="Graphite Gladiator", font=self.font_normal, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)

        self.car_btns = [self.car_1_btn,self.car_2_btn,self.car_3_btn,self.car_4_btn,self.car_5_btn]

        self.chosen_car = 1

        # Przyciski do wyboru mapy

        self.map_pick_text = self.font_large.render("CHOOSE THE MAP", True, (255,255,255))
        self.map_pick_rect = self.map_pick_text.get_rect(center=(960, 550))


        self.map_1_btn = Button(pos=(380,875),text_var="Map Name", font=self.font_normal, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)
        self.map_2_btn = Button(pos=(960,875),text_var="Petrol City", font=self.font_normal, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)
        self.map_3_btn = Button(pos=(1540,875),text_var="Map Name", font=self.font_normal, text_color=(255,255,255),hover_color=(86,86,86),real_screen=self.game.real_screen)

        self.chosen_map = 1

        self.map_btns = [self.map_1_btn,self.map_2_btn,self.map_3_btn]

        # Przycisk do rozpoczęcia gry z wybranym pojazdem oraz mapą

        self.play_button = Button(pos=(960, 955), text_var="START THE RACE", font=self.font_large, text_color=(255,255,255),
                                  hover_color=(86,86,86),real_screen=self.game.real_screen)


    def update(self, events: list[pygame.event.Event]) -> None:

        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time > 200:  # 500ms = 0.5s
            self.car_frame_index = (self.car_frame_index + 1 ) % 16
            self.last_frame_time = current_time

        mouse_pos = pygame.mouse.get_pos()
        self.play_button.changeColor(mouse_pos)

        # Zmiana koloru przycisku odpowiadającemu wybranemu pojazdowi oraz zmiana koloru przycisków wyboru pojazdu po najechaniu na nie

        for index, car_btn in enumerate(self.car_btns,start=1):
            car_btn.text_color=(255,255,255)
            if index == self.chosen_car:
                car_btn.text_color = (86,86,86)
            car_btn.changeColor(mouse_pos)
                  
        # Zmiana koloru przycisku odpowiadającemu wybranej mapie oraz zmiana koloru przycisków wyboru mapy po najechaniu na nie

        for index, map_btn in enumerate(self.map_btns,start=1):
            map_btn.text_color = (255,255,255)
            if index == self.chosen_map:
                map_btn.text_color=(86,86,86)
            map_btn.changeColor(mouse_pos)
           
            

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Rozpoczęcie gry wraz z wybranymi ustawieniami po kliknięciu przycisku 
                if self.play_button.checkForInput(mouse_pos):
                    print("Wybrane auto:",self.chosen_car)
                    print("Wybrana mapa:",self.chosen_map)
                    self.game.selected_map = self.chosen_map - 1
                    self.game.start_race(self.chosen_map, self.chosen_car)

                # Zmiana wybranego auta po kliknięciu przycisku
                for index, car_btn in enumerate(self.car_btns,start=1):
                    if car_btn.checkForInput(mouse_pos):
                        if self.chosen_car!=index:
                            self.chosen_car=index
                            self.car_frame_index = 6
                            self.last_frame_time = pygame.time.get_ticks()

                # Zmiana wybranego auta po kliknięciu na obrazek

                for index, car_img in enumerate(self.car_imgs, start=1):
                    # Sprawdzamy czy kliknięcie miało miejsce wewnątrz obrazka
                    rect = car_img.get_rect(center=(320 + ((index-1) * 320), 300))
                    position = [round(mouse_pos[0] / self.game.real_screen.get_size()[0] * 1920),
                                round(mouse_pos[1] / self.game.real_screen.get_size()[1] * 1080)]
                    if position[0] in range(rect.left, rect.right) and position[1] in range(rect.top,rect.bottom):
                        # Jeśli tak, robimy to samo co w przypadku kliknięcia przycisku
                        if self.chosen_car != index:
                            self.chosen_car = index
                            self.car_frame_index = 6
                            self.last_frame_time = pygame.time.get_ticks()
                
                # Zmiana wybranej mapy po kliknięciu przycisku
                for index, map_btn in enumerate(self.map_btns,start=1):
                    if map_btn.checkForInput(mouse_pos):
                        self.chosen_map=index

                # Zmiana wybranej mapy po kliknięciu na obrazek

                for index, map_img in enumerate(self.map_imgs, start=1):
                    # Sprawdzamy czy kliknięcie miało miejsce wewnątrz obrazka
                    rect = map_img.get_rect(center=(380+((index-1)*580),725))
                    position = [round(mouse_pos[0] / self.game.real_screen.get_size()[0] * 1920),
                                round(mouse_pos[1] / self.game.real_screen.get_size()[1] * 1080)]
                    if position[0] in range(rect.left, rect.right) and position[1] in range(rect.top,rect.bottom):
                        # Jeśli tak, robimy to samo co w przypadku kliknięcia przycisku
                        self.chosen_map = index
                

    def draw(self) -> None:
        # Odpowiednie ustawienie wszystkich przycisków, obrazków oraz napisów na ekranie

        self.play_button.update(self.game.screen)
        for car_btn in self.car_btns:
            car_btn.update(self.game.screen)
        for map_btn in self.map_btns:
            map_btn.update(self.game.screen)
        for index, map_img in enumerate(self.map_imgs):

            map_rect = map_img.get_rect(center=(380+(index*580),725))

            self.game.screen.blit(map_img,map_rect)

        for index, car_imgs in enumerate(self.car_sprites):
            if self.chosen_car-1 == index:    
                car_img = pygame.transform.scale(car_imgs[self.car_frame_index], (300, 300))
            else:
                car_img = pygame.transform.scale(car_imgs[6], (300, 300))
            car_rect = car_img.get_rect(center=(320 + (index * 320), 300))
            self.game.screen.blit(car_img, car_rect)



        self.game.screen.blit(self.map_pick_text, self.map_pick_rect)
        self.game.screen.blit(self.car_pick_text, self.car_pick_rect)
