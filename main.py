import pygame
import random
import math
from vector import Vector
from car import Car


# Wszystkie obroty są w radianach
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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([800, 500])

        self.sprites = [pygame.image.load(f"car-sprites/{i:>04}.png").convert_alpha() for i in range(1, 17)]
        self.clock = pygame.time.Clock()

        self.map = Map(self.screen, "map-image.png", "map-hitbox.png")
        self.init_cars()

    def init_cars(self):
        self.car = Car(self.screen, self.sprites, 0.8, 0.97)
        self.car.map = self.map
        self.car.x = 130
        self.car.y = 130

    def run(self):
        self.running = True
        while self.running:
            self.mainloop()
        pygame.quit()

    def mainloop(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.car.turn_left()
        if keys[pygame.K_RIGHT]:
            self.car.turn_right()
        if keys[pygame.K_UP]:
            self.car.accelerate(0.15)
        if keys[pygame.K_DOWN]:
            self.car.accelerate(-0.15)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
            if event.type == pygame.QUIT:
                self.running = False

        self.car.update()
        self.map.draw_track()
        self.car.draw()
        self.map.draw_background()

        pygame.display.flip()
        self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()

