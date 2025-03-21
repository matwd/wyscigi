import pygame
from barrier import Barrier
from os import path
from hitbox import CircleHitbox
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
