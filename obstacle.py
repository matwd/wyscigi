from hitbox import RectangleHitbox, CircleHitbox
import pygame
from vector import Vector

class Obstacle:
    def __init__(self, game, position, sprite):
        self.game = game
        self.position = position
        self.hitbox = RectangleHitbox(*tuple(position), 0, 100, 60)
        self.sprite = sprite

    def draw(self):
        self.game.screen.blit(self.sprite, (*tuple(self.position - Vector(64, 44)), 128, 128))
        # self.hitbox.draw(self.game.screen)

    def collides(self, position):
        return self.hitbox.check_hit(position)

