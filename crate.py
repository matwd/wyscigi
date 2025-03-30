from __future__ import annotations
from vector import Vector
import math
import pygame
import random
from hitbox import CircleHitbox
from obstacle import Obstacle

class Crate:
    def __init__(self, screen: pygame.surface.Surface, sprite: pygame.surface.Surface, position: Vector) -> None:
        self.screen = screen
        self.sprite = sprite
        self.position = position
        sprite_rectangle = sprite.get_rect()
        self.draw_position = position - Vector(sprite_rectangle.width, sprite_rectangle.height) / 2
        self.hitbox = CircleHitbox(*self.position, 32)

    def draw(self) -> None:
        self.hitbox.draw(self.screen)
        self.screen.blit(self.sprite, tuple(self.draw_position))

    def check_hit(self, point: Vector) -> bool:
        return self.hitbox.check_hit(point)


