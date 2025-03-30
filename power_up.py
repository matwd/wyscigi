from __future__ import annotations
import pygame

class PowerUp:
    sprite_path = None

    def __init__(self, car: Car) -> None:
        self.sprite = pygame.image.load(self.sprite_path)
        self.car = car

    def use(self) -> None:
        "funkcja abstrakcyjna użycia power-upa"
        pass

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self.sprite, (40, 40))

class BananaPeel(PowerUp):
    sprite_path = "assets/banana.png"

    def use(self) -> None:
        self.car.leave_obstacle()
