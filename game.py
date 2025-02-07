import pygame
import random
from main_menu import MainMenu
from end_screen import EndScreen
from car import PlayerCar

class GameState():
    main_menu = 0
    race = 1
    end_screen = 2
    result_screen = 3

debug = True

# Wszystkie obroty są w radianach
class Map:
    def __init__(self, screen, image_filename, hitbox_filename):
        self.screen = screen
        self.hitbox = pygame.image.load(hitbox_filename).convert_alpha()
        self.image = pygame.image.load(image_filename).convert_alpha()

    def is_point_on_track(self, vec):
        rect = self.hitbox.get_rect()
        if 0 < vec.x < rect.width and 0 < vec.y < rect.height:
            return self.hitbox.get_at((int(vec.x), int(vec.y))) == (0, 0, 0, 255)

        return False

    def draw_track(self):
        rect = self.screen.get_rect()
        image_rect = pygame.Rect(0, 0, 800, 500)
        self.screen.blit(self.hitbox, image_rect)

    def draw_background(self):
        rect = self.screen.get_rect()
        image_rect = pygame.Rect(0, 0, 800, 500)
        self.screen.blit(self.image, image_rect)


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode([800, 500])

        self.sprites = [pygame.image.load(f"assets/car-sprites/car-01/{i:>04}.png").convert_alpha() for i in range(1, 17)]
        self.clock = pygame.time.Clock()

        self.time = 0
        self.main_menu = MainMenu(self)
        self.end_screen = EndScreen(self)
        self.state = GameState.main_menu

        self.map = Map(self.screen, "assets/maps/map-01/map-image.png", "assets/maps/map-01/map-hitbox.png")

    def init_cars(self):
        self.cars = []
        self.cars.append(PlayerCar(self.screen, self.sprites, 0.8, 0.97))
        self.cars[0].map = self.map
        self.cars[0].x = 130
        self.cars[0].y = 130

    def run(self):
        self.running = True
        while self.running:
            self.mainloop()
        pygame.quit()

    def start_race(self, map, player_car_sprites):
        self.init_cars()

        self.state = GameState.race

    def end_race(self):
        self.state = GameState.end_screen

    def show_result(self):
        self.state = GameState.main_menu

    def mainloop(self):
        events = pygame.event.get()

        self.screen.fill((0, 0, 0))

        if self.state == GameState.main_menu:
            self.main_menu.update(events)
            self.main_menu.draw()

        elif self.state == GameState.race:
            self.map.draw_track()
            self.map.draw_background()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.end_race()

            for car in self.cars:
                car.update()
                car.draw()

            self.clock.tick(60)

        elif self.state == GameState.end_screen:
            self.end_screen.update(events)
            self.end_screen.draw()

        pygame.display.flip()

        # zamykanie gry
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
            if event.type == pygame.QUIT:
                self.running = False
