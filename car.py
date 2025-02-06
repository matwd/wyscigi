from vector import Vector
import math
import pygame
import random

class Car:
    def __init__(self, screen, sprites, poslizg, tarcie):
        self.screen = screen
        self.sprites = sprites
        self.position = Vector()
        self.velocity = Vector()
        self.rotation_cooldown = 0
        self.direction = 0
        # self.driving = False
        self.rect = self.sprites[0].get_rect()
        self.poslizg = poslizg
        self.tarcie = tarcie
        self.recalculate_hitbox()
        self.update_direction()

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, value):
        self.position.x = value
        self.recalculate_hitbox()

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, value):
        self.position.y = value
        self.recalculate_hitbox()

    def update(self):
        self.reduce_speed(self.tarcie)

        old_position = self.position
        self.position += self.velocity
        self.recalculate_hitbox()

        for p in self.points:
            if not self.map.is_point_on_track(p):
                self.velocity += (self.position - p).normalize() * 0.3
                self.position += old_position
                self.position /= 2
                self.position += (self.position - p) / 10

        point1_outside = not self.map.is_point_on_track(self.points[0])
        point2_outside = not self.map.is_point_on_track(self.points[1])
        point3_outside = not self.map.is_point_on_track(self.points[2])
        point4_outside = not self.map.is_point_on_track(self.points[3])


        if self.direction_vector.scalar_product(self.velocity) > 0:
            if point1_outside:
                self.turn_left()

            if point2_outside:
                self.turn_right()

        else:
            if point3_outside:
                self.turn_right()

            if point4_outside:
                self.turn_left()


        if not self.map.is_point_on_track(self.position):
            self.position = old_position

        self.recalculate_hitbox()
        self.rotation_cooldown -= 1

    def draw(self):
        rect = self.screen.get_rect()
        image_rect = pygame.Rect(self.x-self.rect.width//2, self.y-self.rect.width//2+random.randint(-1, 1), 128, 128)
        self.screen.blit(self.sprites[self.direction], image_rect)

        # pygame.draw.circle(self.screen, pygame.Color('blue'), (self.x, self.y), 3)
        # for p in self.points:
            # pygame.draw.circle(self.screen, pygame.Color('red'), tuple(p), 3)

    def turn_left(self):
        if self.rotation_cooldown <= 0:
            self.rotation_cooldown = 6
            self.direction -= 1
            self.direction %= 16
            self.update_direction()

    def turn_right(self):
        if self.rotation_cooldown <= 0:
            self.rotation_cooldown = 6
            self.direction += 1
            self.direction %= 16
            self.update_direction()

    def update_direction(self):
        degree_in_radians = self.direction / 16 * math.tau
        self.direction_vector = Vector(math.cos(degree_in_radians), math.sin(degree_in_radians))

    def reduce_speed(self, rate):
        self.velocity *= rate

    def accelerate(self, speed):
        self.velocity += speed * self.direction_vector

    def recalculate_hitbox(self):
        forward = self.direction / 16 * math.tau
        point1_rotation = forward + math.pi / 5
        point2_rotation = forward - math.pi / 5
        point3_rotation = forward + math.pi - math.pi / 5
        point4_rotation = forward + math.pi + math.pi / 5
        point1 = self.position + Vector(25 * math.cos(point1_rotation), 15 * math.sin(point1_rotation))
        point2 = self.position + Vector(25 * math.cos(point2_rotation), 15 * math.sin(point2_rotation))
        point3 = self.position + Vector(25 * math.cos(point3_rotation), 15 * math.sin(point3_rotation))
        point4 = self.position + Vector(25 * math.cos(point4_rotation), 15 * math.sin(point4_rotation))
        self.points = [point1, point2, point3, point4]

