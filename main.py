import pygame
import random
import math
from vector import Vector


pygame.init()
screen = pygame.display.set_mode([800, 500])

sprites = [pygame.image.load(f"car-sprites/{i:>04}.png").convert_alpha() for i in range(1, 17)]
clock = pygame.time.Clock()

class Map:
    def __init__(self, screen, image_filename, hitbox_filename):
        self.screen = screen
        self.hitbox = pygame.image.load(hitbox_filename).convert_alpha()
        self.image = pygame.image.load(image_filename).convert_alpha()

    def is_point_on_track(self, vec):
        rect = self.hitbox.get_rect()
        if 0 < vec.x < rect.width and 0 < vec.y < rect.height:
            return self.hitbox.get_at((int(vec.x), int(vec.y))) == (0, 0, 0, 255)

        return False

    def draw_track(self):
        rect = self.screen.get_rect()
        image_rect = pygame.Rect(0, 0, 800, 500)
        self.screen.blit(self.hitbox, image_rect)

    def draw_background(self):
        rect = self.screen.get_rect()
        image_rect = pygame.Rect(0, 0, 800, 500)
        self.screen.blit(self.image, image_rect)


class Car:
    def __init__(self, screen, sprites, poslizg, tarcie):
        self.screen = screen
        self.sprites = sprites
        self.position = Vector()
        self.velocity = Vector()
        self.rotation = 0
        self.direction = 0
        self.driving = False
        self.rect = self.sprites[0].get_rect()
        self.poslizg = poslizg
        self.tarcie = tarcie
        self.recalculate_hitbox()

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

        old_position = car.position
        self.position += self.velocity
        self.recalculate_hitbox()
        angle = self.direction / 16 * math.tau


        for p in self.points[0:1]:
            if not map.is_point_on_track(p):
                print(p, self.position, self.velocity)
                self.velocity += (self.position - p).normalize()

        if True:
            point1_outside = not map.is_point_on_track(self.points[0])
            point2_outside = not map.is_point_on_track(self.points[1])

            if point1_outside:
                self.turn_left(360/16)
                self.reduce_speed(0.30)

            if point2_outside:
                self.turn_right(360/16)
                self.reduce_speed(0.30)


        if not map.is_point_on_track(car.position):
            car.position = old_position

        self.recalculate_hitbox()

    def draw(self):
        rect = self.screen.get_rect()
        image_rect = pygame.Rect(self.x-self.rect.width//2, self.y-self.rect.width//2+random.randint(-1, 1), 128, 128)
        self.screen.blit(self.sprites[self.direction], image_rect)
        pygame.draw.circle(self.screen, pygame.Color('red'), (self.x, self.y), 3)

        for p in self.points[0:1]:
            pygame.draw.circle(self.screen, pygame.Color('red'), tuple(p), 3)

    def turn_left(self, degrees):
        # cały obrót zajmuje 2 sekundy
        self.rotation -= degrees
        self.update_direction()

    def turn_right(self, degrees):
        self.rotation += degrees
        self.update_direction()

    def reduce_speed(self, rate):
        self.velocity *= rate

    def accelerate(self, speed):
        self.velocity.x += speed * math.cos(self.direction / 16 * math.tau)
        self.velocity.y += speed * math.sin(self.direction / 16 * math.tau)

    def update_direction(self):
        degrees = self.rotation
        degrees += 11.25
        self.direction = math.floor((degrees % 360.0) / 360 * 16)

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

car = Car(screen, sprites, 0.8, 0.97)
map = Map(screen, "map-image.png", "map-hitbox.png")
car.x = 130
car.y = 130

running = True
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car.turn_left(3)
    if keys[pygame.K_RIGHT]:
        car.turn_right(3)
    if keys[pygame.K_UP]:
        car.accelerate(0.2)
    if keys[pygame.K_DOWN]:
        car.accelerate(-0.2)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
        if event.type == pygame.QUIT:
            running = False

    car.update()

    map.draw_track()
    car.draw()
    map.draw_background()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
