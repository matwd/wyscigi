import pygame
from barrier import Barrier
from os import path
from hitbox import CircleHitbox, RectangleHitbox
from vector import Vector
from obstacle import Obstacle
import random
import json

# Wszystkie obroty są w radianach
class Map:
    """
    Klasa odpowiedzialna za rysowanie toru gry, zapytania dotyczące
    kolizji z torem, oraz obiekty znajdące się na torze np. przeszkody itp
    """
    # def __init__(self, screen, track_filename, overlay_filename, hitbox_filename, starting_x, starting_y):
    def __init__(self, screen: pygame.surface.Surface) -> None:
        """
        Inicjalizacja obiekty Map, ale bez ładowania tekstur i hitboxów.
        Te muszą zostać załadowane metodą load_from_directory
        """
        self.screen = screen
        self.dimensions = image_rect = pygame.Rect(0, 0, 1920, 1080)
        self.hitbox = None
        self.background = None
        self.overlay = None
        self.enemy_speed = 0
        self.waypoints = []
        self.obstacles = []
        self.progress_rectangles = []
        self.dissapearing_obstacles = []
        self.starting_points = []
        self.barrier = None
        self.starting_x = 440
        self.starting_y = 440

    def load_from_directory(self, map_directory: str, level: int) -> None:
        """
        Matoda ładuje dane o danym torze.
        Argument map_directory to ścieżka do folderu z danymi toru.
        Przykład: "assets/maps/map-01"
        """
        # ładowanie grafik tła, otoczenia oraz hitboxów
        self.hitbox = pygame.image.load(path.join(map_directory, "hitbox.png")).convert()
        self.background = pygame.image.load(path.join(map_directory, "track.png")).convert()
        self.overlay = pygame.image.load(path.join(map_directory, "overlay.png")).convert_alpha()
        obstacle_texture = pygame.image.load("./assets/plama_oleju.png").convert_alpha()

        # czyszczenie tablic
        self.waypoints = []
        self.obstacles = []
        self.progress_rectangles = []
        self.dissapearing_obstacles = []
        self.starting_points = []

        # pobranie danych z jsona do zmiennej map_data
        with open(path.join(map_directory, "data.json")) as file:
            map_data = json.load(file)

        self.enemy_speed = map_data["enemy_speed"]

        # Ładuje punkty do przejechania dla przeciwników
        for waypoint_cords in map_data["waypoints"]:
            self.waypoints.append(CircleHitbox(*waypoint_cords))

        # Ładuje punkty do przejechania dla przeciwników
        random.shuffle(map_data["obstacles"])
        for obstacle_cords in map_data["obstacles"][:2+level]:
            self.obstacles.append(Obstacle(self, Vector(*obstacle_cords), obstacle_texture))

        # Ładowanie szlabanu
        self.barrier = Barrier(*map_data["barrier"])

        # Ładowanie "punktów postępu" sprawdzających czy gracz jedzie poprawnie po torze
        for rectangle_data in map_data["progress_rectangles"]:
            self.progress_rectangles.append(RectangleHitbox(*rectangle_data))

        self.starting_points = map_data["starting_points"]

    def is_point_on_track(self, vec: Vector) -> bool:
        rect = self.hitbox.get_rect()

        # sprawdź czy nie uderzono w szlaban
        if self.barrier.check_hit(vec):
            return False

        # sprawdź czy punkt jest na mapie, jeżeli tak to sprawdź czy jest też na torze
        if 0 < vec.x < rect.width and 0 < vec.y < rect.height:
            return not self.hitbox.get_at((int(vec.x), int(vec.y))) == (255, 255, 255, 255)

        return False

    def get_ground_params(self, vec: Vector) -> tuple[float, float]:
        normal = (0.1, 0.99)
        ice = (0.2, 0.996)
        sand = (0.05, 0.98)
        rect = self.hitbox.get_rect()

        if 0 < vec.x < rect.width and 0 < vec.y < rect.height:
            hitbox_color = self.hitbox.get_at((int(vec.x), int(vec.y)))

            # kolor czarny oznacza normalną trasę
            if hitbox_color == (0, 0, 0, 255):
                return normal

            # kolor biały oznacza teren poza trasą, ale nie obsługujemy kolizji
            # w tym miejscu kodu, więc parametry terenu zostają normalne
            if hitbox_color == (255, 255, 255, 255):
                return normal

            # kolor niebieski to lód (mniejsze tarcie i sterowność)
            if hitbox_color == (0, 0, 255, 255):
                return ice

            # kolor ̣̣żółty oznacza piasek (większe tarcie)
            if hitbox_color == (255, 255, 0, 255):
                return sand

        return normal

    def draw_background(self) -> None:
        self.screen.blit(self.background, (0, 0))
        for obstacle in self.obstacles + self.dissapearing_obstacles:
            obstacle.draw()

    def draw_overlay(self) -> None:
        self.screen.blit(self.overlay, (0, 0))
        if self.barrier:
            self.barrier.draw(self.screen)
