from __future__ import annotations
from vector import Vector
import math
import pygame
import random
from hitbox import CircleHitbox
from obstacle import Obstacle

class Crate:
    def __init__(self, screen: pygame.surface.Surface, sprites: list[pygame.surface.Surface], position: Vector) -> None:
        self.screen = screen
        self.sprites = sprites
        self.position = position
        sprite_rectangle = sprites[0].get_rect()
        self.draw_position = position - Vector(sprite_rectangle.width, sprite_rectangle.height) / 2
        self.hitbox = CircleHitbox(*self.position, 32)
        self.frame = 0

    def draw(self) -> None:
        "funkcja rysuje skrzynkę ale też animuje jej obrót"
        self.frame = (self.frame + 1) % 160
        self.screen.blit(self.sprites[self.frame // 10], tuple(self.draw_position))

    def check_hit(self, point: Vector) -> bool:
        return self.hitbox.check_hit(point)


