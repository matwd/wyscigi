import pygame
import random
import itertools
import json
from os import path
from main_menu import MainMenu
from end_screen import EndScreen
from results_screen import ResultsScreen
from car import PlayerCar, EnemyCar1, EnemyCar2, EnemyCar3
from hitbox import RectangleHitbox, CircleHitbox
from obstacle import Obstacle
from vector import Vector
from game_settings import GameSettings
from barrier import Barrier

class GameState():
    main_menu = 0
    race = 1
    end_screen = 2
    result_screen = 3
    game_settings = 4

debug = True

class Map:
    """
    Klasa odpowiedzialna za rysowanie toru gry, zapytania dotyczące
    kolizji z torem, oraz obiekty znajdące się na torze np. przeszkody itp
    """
    # def __init__(self, screen, track_filename, overlay_filename, hitbox_filename, starting_x, starting_y):
    def __init__(self, screen):
        """
        Inicjalizacja obiekty Map, ale bez ładowania tekstur i hitboxów.
        Te muszą zostać załadowane metodą load_from_directory
        """
        self.screen = screen
        self.dimensions = image_rect = pygame.Rect(0, 0, 1920, 1080)
        self.hitbox = None
        self.background = None
        self.overlay = None
        self.waypoints = []
        self.obstacles = []
        self.dissapearing_obstacles = []
        self.barrier = Barrier(1310, 710, 1.2)
        self.starting_x = 440
        self.starting_y = 440

    def load_from_directory(self, map_directory, level):
        """
        Matoda ładuje dane o danym torze.
        Argument map_directory to ścieżka do folderu z danymi toru.
        Przykład: "assets/maps/map-01"
        """
        self.hitbox = pygame.image.load(path.join(map_directory, "hitbox.png")).convert()
        self.background = pygame.image.load(path.join(map_directory, "track.png")).convert()
        self.overlay = pygame.image.load(path.join(map_directory, "overlay.png")).convert_alpha()
        obstacle_texture = pygame.image.load("./assets/plama_oleju.png").convert_alpha()
        with open(path.join(map_directory, "data.json")) as file:
            data = json.load(file)

            # Ładuje punkty do przejechania dla przeciwników
            for waypoint_cords in data["waypoints"]:
                self.waypoints.append(CircleHitbox(*waypoint_cords))

            # Ładuje punkty do przejechania dla przeciwników
            random.shuffle(data["obstacles"])
            for obstacle_cords in data["obstacles"][:2+level]:
                self.obstacles.append(Obstacle(self, Vector(*obstacle_cords), obstacle_texture))

    def is_point_on_track(self, vec):
        rect = self.hitbox.get_rect()

        # sprawdź czy nie uderzono w szlaban
        if self.barrier.check_hit(vec):
            return False

        # sprawdź czy punkt jest na mapie, jeżeli tak to sprawdź czy jest też na torze
        if 0 < vec.x < rect.width and 0 < vec.y < rect.height:
            return self.hitbox.get_at((int(vec.x), int(vec.y))) == (0, 0, 0, 255)

        return False

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))
        for obstacle in self.obstacles + self.dissapearing_obstacles:
            obstacle.draw()

    def draw_overlay(self):
        self.screen.blit(self.overlay, (0, 0))
        if self.barrier:
            self.barrier.draw(self.screen)

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

        self.real_screen = pygame.display.set_mode([1920, 1080], pygame.RESIZABLE)

        self.screen = pygame.Surface([1920, 1080])

        self.font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 40)

        self.sprites = [pygame.image.load(f"assets/car-sprites/car-01/{i:>04}.png").convert_alpha() for i in range(1, 17)]
        self.sprites = [pygame.transform.scale(s, (128, 128)) for s in self.sprites]
        self.clock = pygame.time.Clock()

        self.time = 0
        self.main_menu = MainMenu(self)
        self.end_screen = EndScreen(self)
        self.results_screen = ResultsScreen(self)
        self.game_settings = GameSettings(self)
        self.state = GameState.main_menu

        self.map = Map(self.screen)
        self.progress_rectangles = [
            RectangleHitbox(1200, 150, 0, 300, 200),
            RectangleHitbox(200, 650, 0, 400, 500),
            RectangleHitbox(1750, 400, 0, 250, 200),
        ]

        self.music = pygame.mixer.music

        self.show_main()

    def init_cars(self):
        self.cars = []
        self.cars.append(PlayerCar(self, self.sprites, 0.1, 0.99))
        self.cars.append(EnemyCar1(self, self.sprites, 0.1, 0.99))
        self.cars.append(EnemyCar2(self, self.sprites, 0.1, 0.99))
        self.cars.append(EnemyCar3(self, self.sprites, 0.1, 0.99))

        for car in self.cars:
            car.map = self.map
            car.x = self.map.starting_x
            car.y = self.map.starting_y
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

        self.map.load_from_directory(f"assets/maps/map-{map:02}", map)

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
            self.map.barrier.update()

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.end_race()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)

            self.update_cars()

            self.map.draw_overlay()

            self.time += 1000 / 60
            text_surface, ract = self.font.render(self.ms_to_sec(self.time), pygame.color.THECOLORS["white"])
            self.screen.blit(text_surface, (self.screen.get_width() - 100 - ract.width, 100))


        elif self.state == GameState.end_screen:
            self.end_screen.update(events)
            self.end_screen.draw()

        elif self.state == GameState.result_screen:
            self.results_screen.update(events)
            self.results_screen.draw()

        elif self.state == GameState.game_settings:
            self.game_settings.update(events)
            self.game_settings.draw()

        self.real_screen.blit(pygame.transform.scale(self.screen, self.real_screen.get_size()), (0, 0))
        pygame.display.flip()

        # zamykanie gry
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
            if event.type == pygame.QUIT:
                self.running = False

    def draw_debug(self):
        for car in self.cars:
            car.draw_debug()
        for i in self.progress_rectangles:
            i.draw(self.screen)
        for d in self.map.waypoints:
            d.draw(self.screen)

    def update_cars(self):
        self.cars.sort(key=lambda x: x.position.y)
        for car in self.cars:
            car.update()
            car.draw()

            for obstacle in self.map.obstacles:
                if car.spin <= 0 and obstacle.collides(car.position) and car.velocity.length() > 5:
                    car.spin = 16*2
                    car.reduce_speed(0.1)

            for obstacle in self.map.dissapearing_obstacles:
                if car.spin <= 0 and obstacle.collides(car.position) and car.velocity.length() > 5:
                    car.spin = 16*2
                    car.reduce_speed(0.1)
                    self.map.dissapearing_obstacles.remove(obstacle)
                    break

            if self.progress_rectangles[car.track_progress].check_hit(car.position):
                car.track_progress += 1
                if car.track_progress == len(self.progress_rectangles):
                    car.okrazenie += 1
                    car.track_progress = 0
                    if car.okrazenie == 3 and isinstance(car, PlayerCar):
                        self.end_race()


        for car1, car2 in itertools.combinations(self.cars, 2):
            intersecting = False
            for point in car2.hitbox.get_points() + (car2.position,):
                if car1.hitbox.check_hit(point):
                    intersecting = True
            for point in car1.hitbox.get_points() + (car1.position,):
                if car2.hitbox.check_hit(point):
                    intersecting = True
            if intersecting:
                diff = car1.position - car2.position
                car1.position += diff * 0.05
                car2.position += -diff * 0.05
                car1.reduce_speed(0.9)
                car2.reduce_speed(0.9)

