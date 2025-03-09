import pygame
import random
from main_menu import MainMenu
from end_screen import EndScreen
from results_screen import ResultsScreen
from car import PlayerCar, EnemyCar1, EnemyCar2, EnemyCar3
from hitbox import RectangleHitbox, CircleHitbox
from obstacle import Obstacle
from vector import Vector
from game_settings import GameSettings

class GameState():
    main_menu = 0
    race = 1
    end_screen = 2
    result_screen = 3
    game_settings = 4

debug = True

# Wszystkie obroty są w radianach
class Map:
    """
    Klasa odpowiedzialna za rysowanie toru gry i zapytania dotyczące
    kolizji z torem
    """
    def __init__(self, screen, track_filename, overlay_filename, hitbox_filename):
        self.screen = screen
        self.hitbox = pygame.image.load(hitbox_filename).convert()
        self.background = pygame.image.load(track_filename).convert()
        self.overlay = pygame.image.load(overlay_filename).convert_alpha()
        self.dimensions = image_rect = pygame.Rect(0, 0, 1920, 1080)

    def is_point_on_track(self, vec):
        rect = self.hitbox.get_rect()
        if 0 < vec.x < rect.width and 0 < vec.y < rect.height:
            return self.hitbox.get_at((int(vec.x), int(vec.y))) == (0, 0, 0, 255)

        return False

    def draw_background(self):
        self.screen.blit(self.background, self.dimensions)

    def draw_overlay(self):
        self.screen.blit(self.overlay, self.dimensions)

class Game:
    """
    Klasa gry. Obsługuje pętle główną i zamykanie okna gry
    """
    def __init__(self):
        # Inicjalizowanie biblioteki pygame i otworzenie okna
        pygame.init()
        pygame.font.init()

        self.sound = True
        try:
            pygame.mixer.init()
        except pygame.error:
            print("brak wyjścia audio")
            self.sound = False
            
        self.real_screen = pygame.display.set_mode([1440, 810], pygame.RESIZABLE)

        self.screen = pygame.Surface([1920, 1080])

        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 40)

        self.sprites = [pygame.image.load(f"assets/car-sprites/car-01/{i:>04}.png").convert_alpha() for i in range(1, 17)]
        self.clock = pygame.time.Clock()

        self.time = 0
        self.main_menu = MainMenu(self)
        self.end_screen = EndScreen(self)
        self.results_screen = ResultsScreen(self)
        self.game_settings = GameSettings(self)
        self.state = GameState.main_menu

        self.map = Map(self.screen, "assets/maps/map-01/track.png", "assets/maps/map-01/overlay.png", "assets/maps/map-01/hitbox.png")
        self.progress_rectangles = [
            RectangleHitbox(1200, 150, 0, 300, 200),
            RectangleHitbox(200, 650, 0, 400, 500),
            RectangleHitbox(1750, 400, 0, 250, 200),
        ]
        self.music = pygame.mixer.music
        obstacle_texture = pygame.image.load("./assets/plama_oleju.png").convert_alpha()
        self.obstacles = [
            Obstacle(self, Vector(1000, 200), obstacle_texture),
            Obstacle(self, Vector(1200, 140), obstacle_texture),
        ]

        self.show_main()

    def init_cars(self):
        self.cars = []
        self.cars.append(PlayerCar(self, self.sprites, 0.1, 0.99))
        self.cars.append(EnemyCar1(self, self.sprites, 0.1, 0.99))
        self.cars.append(EnemyCar2(self, self.sprites, 0.1, 0.99))
        self.cars.append(EnemyCar3(self, self.sprites, 0.1, 0.99))

        for car in self.cars:
            car.map = self.map
            car.x = 460
            car.y = 460
            car.okrazenie = 0
            car.track_progress = 0


    def run(self):
        """
        Gra po uruchomieniu wywołuje pętlę główną gry 60 razy na sekundę
        aż do ustawienia zmienner self.running na False
        """
        self.running = True
        while self.running:
            self.mainloop()

            a = self.clock.tick(60)
            # print(a)
        pygame.quit()

    def open_settings(self):
        self.state = GameState.game_settings

    def start_race(self, map, player_car_sprites):
        self.init_cars()

        if self.sound:
            self.music.stop()
            self.music.unload()

            self.music.load("./assets/music/level_1.mp3")
            self.music.play(-1)

        self.state = GameState.race

    def end_race(self):
        # self.time = random.randint(2000, 5000) / 100
        self.state = GameState.end_screen

    def show_result(self):
        self.state = GameState.result_screen

    def show_main(self):
        if self.sound:
                
            self.music.stop()
            self.music.unload()

            self.music.load("assets/music/level_3.ogg")
            self.music.play(-1)

        self.state = GameState.main_menu

    def ms_to_sec(self, ms):
        ms = int(ms)
        seconds = ms // 1000
        ms = ms % 1000
        return f"{seconds}.{ms}"

    def mainloop(self):
        events = pygame.event.get()

        self.screen.fill((0, 0, 0))

        if self.state == GameState.main_menu:
            self.main_menu.update(events)
            self.main_menu.draw()

        elif self.state == GameState.race:
            self.map.draw_background()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.end_race()

            for obstacle in self.obstacles:
                obstacle.draw()

            for car in self.cars:
                car.update()
                car.draw()

                for obstacle in self.obstacles:
                    if car.spin <= 0 and obstacle.collides(car.position) and car.velocity.length() > 5:
                        car.spin = 16*2
                        car.reduce_speed(0.1)

                if self.progress_rectangles[car.track_progress].check_hit(car.position):
                    car.track_progress += 1
                    if car.track_progress == len(self.progress_rectangles):
                        car.okrazenie += 1
                        car.track_progress = 0
                        if car.okrazenie == 3 and isinstance(car, PlayerCar):
                            self.end_race()

            self.map.draw_overlay()

            self.time += 1000 / 60
            text_surface, ract = self.font.render(self.ms_to_sec(self.time), pygame.color.THECOLORS["white"])
            self.screen.blit(text_surface, (self.screen.get_width() - 100 - ract.width, 100))
            # for i in self.progress_rectangles:
                # i.draw(self.screen)


        elif self.state == GameState.end_screen:
            self.end_screen.update(events)
            self.end_screen.draw()

        elif self.state == GameState.result_screen:
            self.results_screen.update(events)
            self.results_screen.draw()

        elif self.state == GameState.game_settings:
            self.game_settings.update(events)
            self.game_settings.draw()

        self.real_screen.blit(pygame.transform.scale(self.screen, self.real_screen.get_size()), (0, 0, *self.real_screen.get_size()))
        pygame.display.flip()

        # zamykanie gry
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
            if event.type == pygame.QUIT:
                self.running = False
