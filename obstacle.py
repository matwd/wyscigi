from __future__ import annotations
from hitbox import RectangleHitbox, CircleHitbox
import pygame
from vector import Vector

class Obstacle:
    """
    Klasa reprezentuje przeszkody na torze takie jak kałuże
    oleju i skórki od banan
    """
    def __init__(self, game: Game, position: Vector, sprite: pygame.surface.Surface) -> None:
        self.game = game
        self.position = position
        self.hitbox = RectangleHitbox(*tuple(position), 0, 100, 60)
        self.sprite = sprite

    def draw(self) -> None:
        "Rysowanie przeszkody"
        self.game.screen.blit(self.sprite, (*tuple(self.position - Vector(64, 44)), 128, 128))

    def draw_debug(self) -> None:
        "Rysowanie hitbox przeszkody"
        self.hitbox.draw(self.game.screen)

    def collides(self, position) -> bool:
        "Funkcja do sprawdzania czy auto wjechało w przeszkodę"
        return self.hitbox.check_hit(position)

