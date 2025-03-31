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
        # hitbox przeszkody jest oparty na jej sprite
        sprite_rect = sprite.get_rect()
        self.draw_position = position - Vector(sprite_rect.width, sprite_rect.height) / 2
        self.hitbox = RectangleHitbox(*tuple(position), 0, sprite_rect.width, sprite_rect.height)
        self.sprite = sprite

    def draw(self) -> None:
        "Rysowanie przeszkody"
        self.hitbox.draw(self.game.screen)
        self.game.screen.blit(self.sprite, tuple(self.draw_position))

    def draw_debug(self) -> None:
        "Rysowanie hitbox przeszkody"
        self.hitbox.draw(self.game.screen)

    def collides(self, position) -> bool:
        "Funkcja do sprawdzania czy auto wjechało w przeszkodę"
        return self.hitbox.check_hit(position)

