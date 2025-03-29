import pygame
import random
import itertools
from main_menu import MainMenu
from end_screen import EndScreen
from results_screen import ResultsScreen
from car import PlayerCar, EnemyCar1, EnemyCar2, EnemyCar3, EnemyCar4
from snowfall import Snowfall
from game_settings import GameSettings
from countdown import CountdownScreen
from map import Map

class GameState():
    """
    Klasa/Enum używany do obsługi obecnego stanu gry
    """
    # główne menu
    main_menu = 0
    # wybór opcji gry
    game_settings = 1
    # odliczanie do zaczecia gry
    starting_countdown = 2
    # trwa wyścig
    race = 3
    # zakończenie wyścigu
    end_screen = 4
    # ekran z wynikami
    result_screen = 5

debug = True

class Game:
    """
    Klasa gry. Obsługuje pętle główną i zamykanie okna gry
    """
    def __init__(self) -> None:
        # Inicjalizowanie biblioteki pygame i otworzenie okna
        pygame.init()
        pygame.font.init()

        # Inicjalizacja dźwięku
        self.sound = True
        try:
            pygame.mixer.init()
        except pygame.error:
            # jeżeli nie znaleziono głośnika to wyłączamy dźwięk
            print("brak wyjścia audio")
            self.sound = False

        # ustawienie ikony okna
        icon = pygame.image.load('assets/logo.ico') 
        pygame.display.set_icon(icon)

        # otwarcie okna gry
        self.real_screen = pygame.display.set_mode([1920, 1080], pygame.RESIZABLE)

        # Tekstura na którą wszystko jest rysowane
        # jest potem skalowana do rozmiaru okna gry
        self.screen = pygame.Surface([1920, 1080])

        # inicjalizacja czcionki
        self.font = pygame.font.Font("assets/font/Jersey10.ttf", 40)

        # ładowanie spritów samochodzików z katalogu assets/car-sprites
        # dla każdego auta ładujemy 16 obrazków z odpowiednigo katalogu
        self.sprites = [
            [pygame.image.load(f"assets/car-sprites/car-01/{i:>04}.png") for i in range(1, 17)],
            [pygame.image.load(f"assets/car-sprites/car-02/{i:>04}.png") for i in range(1, 17)],
            [pygame.image.load(f"assets/car-sprites/car-03/{i:>04}.png") for i in range(1, 17)],
            [pygame.image.load(f"assets/car-sprites/car-04/{i:>04}.png") for i in range(1, 17)],
            [pygame.image.load(f"assets/car-sprites/car-05/{i:>04}.png") for i in range(1, 17)]
        ]

        # skalowanie obrazków do odpowiedniego rozmiaru
        self.sprites = [[pygame.transform.scale(s, (128, 128)).convert_alpha(self.screen) for s in car_sprites] for car_sprites in self.sprites]

        # utworzenie zegara pozwalającego uzyskać stabilną (w miarę możliwości systemu) liczbę klatek na sekundę
        # oraz tablice mierzące czas przejechania okrążeń
        self.clock = pygame.time.Clock()
        self.time = 0
        self.lap_times = [0, 0, 0]

        # zainicjalizowanie ekranów menu, ustawień wyścigu, końcowego i wyników
        self.main_menu = MainMenu(self)
        self.game_settings = GameSettings(self)
        self.end_screen = EndScreen(self)
        self.results_screen = ResultsScreen(self)
        self.countdown_screen = CountdownScreen(self)

        # inicjalizacja efektu opadania śniegu
        self.snowfall = Snowfall(-10, 20, 1.25, 2, 1920, 1080)

        self.selected_map = 0

        self.map = Map(self.screen)

        self.music = pygame.mixer.music

        self.show_main()

    def init_cars(self, player_car_sprite: int) -> None:
        self.cars = []

        sprites = self.sprites.copy()

        self.cars.append(PlayerCar(self, sprites.pop(player_car_sprite),0.2))

        random.shuffle(sprites)

        self.cars.append(EnemyCar1(self, sprites.pop(), 0.2, self.map.waypoints))
        self.cars.append(EnemyCar2(self, sprites.pop(), 0.2, self.map.waypoints))
        self.cars.append(EnemyCar3(self, sprites.pop(), 0.2, self.map.waypoints))
        self.cars.append(EnemyCar4(self, sprites.pop(), 0.2, self.map.waypoints))

        for i, car in enumerate(self.cars):
            car.map = self.map
            car.x, car.y, car.direction = self.map.starting_points[i]

            car.okrazenie = 0
            car.track_progress = 0


    def run(self) -> None:
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

    def open_settings(self) -> None:
        self.state = GameState.game_settings

    def start_countdown(self, map: Map, chosen_car: int) -> None:
        if self.sound:
            self.music.stop()
            self.music.unload()

            self.music.load("./assets/music/level_1.mp3")
            self.music.play(-1)
        self.state = GameState.starting_countdown
        self.selected_map = map
        self.map.load_from_directory(f"assets/maps/map-{map:02}", map)

        self.init_cars(chosen_car-1)

    def start_race(self) -> None:
        
        self.lap_times = [0, 0, 0]


        

        self.state = GameState.race

    def end_race(self) -> None:
        self.state = GameState.end_screen

    def show_result(self) -> None:
        self.state = GameState.result_screen

    def show_main(self) -> None:
        if self.sound:

            self.music.stop()
            self.music.unload()

            self.music.load("assets/music/menu.mp3")
            self.music.play(-1)

        self.state = GameState.main_menu

    def ms_to_sec(self, ms: float) -> str:
        ms = int(ms)
        seconds = ms // 1000
        ms = ms % 1000
        return f"{seconds}.{ms}"

    def mainloop(self) -> None:
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
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LCTRL] and keys[pygame.K_F1]:
                        self.end_race()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event.pos)

            self.update_cars()

            self.map.draw_overlay()

            if self.selected_map == 3:
                self.snowfall.snowfall(self.screen, random.random() - 0.5)

            self.time += 1000 / 60
            text_surface = self.font.render(self.ms_to_sec(self.time), True, (255, 255, 255))
            # self.screen.blit(text_surface, (self.screen.get_width() - 100 - text_surface.get_width(), 100))

            player = filter(lambda x: isinstance(x, PlayerCar), self.cars).__iter__().__next__()

            if player.okrazenie < 3:
                self.lap_times[player.okrazenie] += 1000 / 60

            screen_width = self.screen.get_width()

            for i, time in enumerate(self.lap_times):
                time_color = (123, 123, 123)
                if (i == player.okrazenie):
                    time_color = (255, 255, 255)

                time_surface = self.font.render(self.ms_to_sec(time), True, time_color)    
                time_width = time_surface.get_width()

                space_for_time_text = 150

                self.screen.blit(time_surface, (screen_width / 2 - time_width / 2 + space_for_time_text * (i - 1), 25))

            lap_surface = self.font.render(f"{player.okrazenie + 1}/3", True, (255, 255, 255))
            self.screen.blit(lap_surface, (screen_width - lap_surface.get_width() - 25, 25))


            # self.draw_debug()


        elif self.state == GameState.end_screen:
            self.end_screen.update(events)
            self.end_screen.draw()

        elif self.state == GameState.result_screen:
            self.results_screen.update(events)
            self.results_screen.draw()

        elif self.state == GameState.game_settings:
            self.game_settings.update(events)
            self.game_settings.draw()
        
        elif self.state == GameState.starting_countdown:
            self.countdown_screen.update(events)
            self.countdown_screen.draw()

        self.real_screen.blit(pygame.transform.scale(self.screen, self.real_screen.get_size()), (0, 0))
        pygame.display.flip()

        # zamykanie gry
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.QUIT:
                self.running = False

    def draw_debug(self) -> None:
        for car in self.cars:
            car.draw_debug()
        for i in self.map.progress_rectangles:
            i.draw(self.screen)
        for d in self.map.waypoints:
            d.draw(self.screen)

    def update_cars(self) -> None:
        self.cars.sort(key=lambda x: x.position.y)
        for car in self.cars:
            car.update()
            car.draw()

            for obstacle in self.map.obstacles:
                if car.spin <= 0 and obstacle.collides(car.position) and car.velocity.length() > 5:
                    car.spin = 16*2
                    if self.sound:
                        pygame.mixer.Sound("assets/sfx/poslizg.mp3").play()
                    car.reduce_speed(0.1)

            for obstacle in self.map.dissapearing_obstacles:
                if car.spin <= 0 and obstacle.collides(car.position) and car.velocity.length() > 5:
                    car.spin = 16*2
                    car.reduce_speed(0.1)
                    self.map.dissapearing_obstacles.remove(obstacle)
                    break

            if self.map.progress_rectangles[car.track_progress].check_hit(car.position):
                car.track_progress += 1
                if car.track_progress == len(self.map.progress_rectangles):
                    car.okrazenie += 1
                    car.track_progress = 0

                    # if isinstance(car, PlayerCar):
                    #     self.lap_times.append(self.time - sum(self.lap_times))

                    if car.okrazenie == 3 and isinstance(car, PlayerCar):
                        self.end_race()


        for car1, car2 in itertools.combinations(self.cars, 2):
            intersecting = False
            if (car1.position - car2.position).length() > 100:
                # jezeli auta są daleko od siebie to nie sprawdzamy kolizji
                continue
            car1_points = car1.hitbox.get_points()
            car1_points += tuple((car1_points[i] + car1_points[i+1]) / 2 for i in range(-1, 3))
            for point in car2.hitbox.get_points() + (car2.position,):
                if car1.hitbox.check_hit(point):
                    intersecting = True
            for point in car1_points:
                if car2.hitbox.check_hit(point):
                    intersecting = True
            if intersecting:
                diff = car1.position - car2.position
                car1.position += diff * 0.05
                car2.position += -diff * 0.05
                car1.recalculate_hitbox()
                car2.recalculate_hitbox()
                car1.reduce_speed(0.9)
                car2.reduce_speed(0.9)

