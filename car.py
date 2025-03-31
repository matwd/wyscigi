from __future__ import annotations
from vector import Vector
import math
import pygame
import random
from hitbox import RectangleHitbox
from obstacle import Obstacle
import pygame.gfxdraw
from power_up import BananaPeel, Ghost

class Car:
    "Klasa Samochodu z której dziedziczą klasy gracza i przeciwników"
    def __init__(self, game: Game, sprites: list[pygame.surface.Surface], speed: float) -> None:
        self.game = game
        self.sprites = sprites
        self.speed = speed
        # poślizg i tarcie są aktualizowane później zależnie od terenu po którym jedzie samochów
        self.poslizg = 0
        self.tarcie = 1
        self.position = Vector()
        self.velocity = Vector(0, 0)
        self.rotation_cooldown = 0
        self._direction = 0
        self.spin = 0
        self.nitro = 100
        self.hitbox = RectangleHitbox(self.x, self.y, 0, 80, 36)
        self.power_up = None
        self.ghost_cooldown = 0

    # getter i setter dla kierunku
    # tak jak w grach retro samochód może być oburcony w ograniczoną ilość kierunków
    # u nas jest to 16 kierunków
    @property
    def direction(self) -> int:
        return self._direction

    @direction.setter
    def direction(self, value: int) -> None:
        # ustawia kierunek (jeden z 16 możliwych) i wektor kierunku
        self._direction = value
        # Zapisuje w właściwości degree_vector kierunek jako wektor
        degree_in_radians = self.direction / 16 * math.tau
        self.direction_vector = Vector(math.cos(degree_in_radians), math.sin(degree_in_radians))
        self.recalculate_hitbox()

    # poniżej są gettery i settery dla współrzędnych x i y
    @property
    def x(self) -> int:
        return self.position.x

    @x.setter
    def x(self, value: int) -> None:
        self.position.x = value
        self.recalculate_hitbox()

    @property
    def y(self: int) -> None:
        return self.position.y

    @y.setter
    def y(self, value: int) -> None:
        self.position.y = value
        self.recalculate_hitbox()

    def is_ghost(self) -> bool:
        "Sprawdza czy samochód obecnie jest duchem"
        return self.ghost_cooldown > 0

    def is_going_forward(self) -> bool:
        """
        Sprawdza czy samochód porusza się do przodu
        Korzystamy tu z matematycznych właściwości iloczynu wektorowego
        Jeżeli kąt między dwoma wektorami jest mniejszy niż 90 stopni
        to iloczyn wektorowy jest większy niż 0
        """
        return self.direction_vector.scalar_product(self.velocity) > 0

    def update(self) -> None:
        "Aktualizacja fizyki samochodu w każdej klatce"
        # zwolnienie w zależności od tarcia
        self.reduce_speed(self.tarcie)

        # przesuwamy samochód w zależności od jego prędkości
        old_position = self.position
        self.position += self.velocity
        self.recalculate_hitbox()

        # jeżeli samochód jest w trakcie obrotu z powodu kałuży to się obraca
        if self.spin > 0:
            if self.spin % 2 == 0:
                self.direction += 1
                self.direction %= 16
            self.spin -= 1

        points = self.hitbox.get_points()

        is_ghost = self.ghost_cooldown > 0
        for p in points:
            if not self.map.is_point_on_track(p, is_ghost):
                self.velocity += (self.position - p).normalize() * 0.2
                self.position += (self.position - p) * 0.05
                self.velocity *= 0.91

        point1_outside = not self.map.is_point_on_track(points[0], is_ghost)
        point2_outside = not self.map.is_point_on_track(points[1], is_ghost)
        point3_outside = not self.map.is_point_on_track(points[2], is_ghost)
        point4_outside = not self.map.is_point_on_track(points[3], is_ghost)

        if self.is_going_forward():
            if point1_outside:
                self.turn_right()

            if point2_outside:
                self.turn_left()

        else:
            if point3_outside:
                self.turn_right()

            if point4_outside:
                self.turn_left()

        ground_params = self.map.get_ground_params(self.position)
        # print(ground_params)
        self.poslizg = ground_params[0]
        self.tarcie = ground_params[1]

        if self.nitro < 100:
            self.nitro += 0.1

        if self.ghost_cooldown > 0:
            self.ghost_cooldown -= 1

        self.recalculate_hitbox()
        self.rotation_cooldown -= 1

    def draw(self) -> None:
        "Rysowanie samochodu"
        rect = self.sprites[0].get_rect()
        image_rect = pygame.Rect(self.x-rect.width/2, self.y-rect.width/2+random.randint(-1, 1), 256, 256)
        if self.is_ghost():
            self.game.screen.blit(self.sprites[self.direction], image_rect, special_flags=pygame.BLEND_ADD)
        else:
            self.game.screen.blit(self.sprites[self.direction], image_rect)

        self.hitbox.pos = self.position.copy()

    def draw_debug(self) -> None:
        "Rysowanie hitboxa samochodu (Funkcja do debugowania)"
        self.hitbox.draw(self.game.screen)
        pygame.draw.circle(self.game.screen, pygame.Color('red'), (self.x, self.y), 3)


    def turn_left(self) -> None:
        "Skręcanie w lewo"
        if self.rotation_cooldown <= 0 and self.spin <= 0:
            self.velocity = self.velocity.rotate(-0.4 + self.poslizg)
            self.rotation_cooldown = 7
            self.direction -= 1
            self.direction %= 16

    def turn_right(self) -> None:
        "Skręcanie w prawo"
        if self.rotation_cooldown <= 0 and self.spin <= 0:
            self.velocity = self.velocity.rotate(0.4 - self.poslizg)
            self.rotation_cooldown = 7
            self.direction += 1
            self.direction %= 16

    def reduce_speed(self, rate: float) -> None:
        "Zmniejsza prędkość gracz. Używane do symulowania tarcie"
        self.velocity *= rate

    def accelerate(self, rate: float) -> None:
        "Przyspiesza gracza w kierunku w który jest skierowany"
        self.velocity += self.speed * rate * self.direction_vector

    def recalculate_hitbox(self) -> None:
        "Przesuwa i obraca hitbox po przesunięciu lub obrocie gracza"
        forward = self.direction / 16 * math.tau
        self.hitbox.rotation = forward
        self.hitbox.position = self.position.copy()

    def leave_obstacle(self) -> None:
        "Zostawia na ziemi przeszkodę (banana)"
        banana_texture = pygame.image.load("./assets/banana.png").convert_alpha()
        self.game.map.dissapearing_obstacles.append(Obstacle(self.game, self.position - self.direction_vector.normalize() * 60, banana_texture))

    def get_random_power_up(self) -> None:
        power_ups = [BananaPeel(self),Ghost(self)]
        random.shuffle(power_ups)
        self.power_up = power_ups[0]

class PlayerCar(Car):
    "Klasa auta gracza"
    def update(self) -> None:
        super().update()
        # jażeli gracz wpadł w przeszkodę to nie może skręcać
        if self.spin > 0:
            return

        # Jeżdzenie samochodzikiem
        keys = pygame.key.get_pressed()
        # skręcanie w lewo
        # klawisze: strzałka w lewo lub A
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.turn_left()
        # skręcanie w prawo
        # klawisze: strzałka w prawo lub D
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.turn_right()
        # jazda do przodu
        # klawisze: strzałka do przodu lub W
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.accelerate(1)
        # jazda do tyłu
        # klawisze: strzałka do tyłu lub S
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.accelerate(-1)
        # przyspieszenie nitro
        # klawisze: spacja
        if keys[pygame.K_SPACE]:
            if self.nitro >= 10:
                self.nitro -= 5
                self.accelerate(3)
        # Zostawienie przeszkody na torze (jeżeli dostępna)
        # klawisze: E
        if keys[pygame.K_e]:
            if self.power_up:
                self.power_up.use()
                self.power_up = None

    def draw_stats(self) -> None:
        "rysowanie kółka z obecnym power-upem w lewym górnym rogu ekranu"
        pygame.gfxdraw.filled_circle(self.game.screen, 70, 70, 64, (0, 0, 0, 127))
        if self.power_up:
            self.power_up.draw(self.game.screen)

        pygame.draw.rect(self.game.screen, (0, 0, 0), (160, 20, 200, 20), border_radius=4)
        pygame.draw.rect(self.game.screen, (0, 0, 240), (160, 20, self.nitro * 2, 20), border_radius=4)


class EnemyCar(Car):
    "Klasa abstrakcyjna dla wszystkich przeciwników"
    def __init__(self, game: Game, sprites: list[pygame.surface.Surface], speed: float, waypoints: list[CircleHitbox]) -> None:
        """
        Funkcja inicjalizująca samochodu przyjmuje również listę
        punktów po których przeciwnik jeździ w kółko
        """
        super().__init__(game, sprites, speed)
        self.waypoints = waypoints
        self.next_target = 0

    def update(self) -> None:
        super().update()
        # jeżeli gracz przejedzie przez jakikolwiek waypoint
        # to ustawia kolejny waypoint na swój cel
        for i, w in enumerate(self.waypoints):
            if w.check_hit(self.position):
                self.next_target = (i + 1) % len(self.waypoints)
        # target = self.waypoints[self.next_target]
        # if target.check_hit(self.position):
        #     self.next_target = (self.next_target + 1) % len(self.waypoints)

    def turn_to_target(self, target: Vector) -> None:
        "Obróć się do celu i jedź do niego"

        # obliczenie kierunku w który przeciwnik powinien jechać
        wanted_direction = target - self.position
        angle_to_target = math.atan2(wanted_direction.y, wanted_direction.x) + (math.tau/32)
        target_rotation = int(angle_to_target // (math.tau/16)) % 16

        # Skręcenie w lewo lub prawo w zależności od tego w którą
        # stronę trzeba skręcać krócej, żeby obrócić się w strinę celu
        if self.direction != target_rotation:
            if ((target_rotation - self.direction) % 16) < 8:
                self.turn_right()
            else:
                self.turn_left()

        # jeżeli samochód jest odwrócony w stronę celu
        if self.direction == target_rotation:
            # jeżeli jest blisko to hamuje
            if wanted_direction.length() < 120 and self.velocity.length() > 4:
                pass
            # jeżeli daleko to przyspiesza
            else:
                self.accelerate(1)

class EnemyCar1(EnemyCar):
    def update(self) -> None:
        super().update()

        # pierwszy przeciwnik poprostu jedzie w stronę kolejnego celu
        target = self.waypoints[self.next_target]
        self.turn_to_target(target.position)

    def draw(self):
        super().draw()

class EnemyCar2(EnemyCar):
    close_wall_check_cooldown = 0

    def update(self) -> None:
        super().update()

        # pierwsza część logiki kierowania
        # sprawdzenie czy samochód jedzie mniej więcej w stronę kolejnego punktu
        target = self.waypoints[self.next_target]
        wanted_direction = target.position - self.position
        angle_to_target = math.atan2(wanted_direction.y, wanted_direction.x) + (math.tau/32)
        target_rotation = int(angle_to_target // (math.tau/16)) % 16
        needed_rotation = (self.direction - target_rotation) % 16

        if needed_rotation in (0, 1, 2, 3, 15, 14, 13):
            pass
        elif needed_rotation < 8:
            self.turn_left()
            self.accelerate(1)
            return
        elif needed_rotation > 8:
            self.turn_right()
            self.accelerate(1)
            return


        # druga część logiki kierowania

        # wybieramy 5 kierunków (w lewo, troche w lewo, przed samochód, troche w prawo, w prawo)
        directions = [
            (self.direction + off) / 16 * math.tau for off in range(-2, 3)
        ]
        # wysłanie promieni w tych kierunkach
        lidar = [
            self.ray_march(self.position, Vector(1, 0).rotate(d)) for d in directions
        ]

        lidar = [(i - self.position).length() for i in lidar]

        # odliczenie odległości dla obydwu kierunków po lewej
        # centrum i obydwu kierunków po prawej
        left = (lidar[0] + lidar[1]) / 2
        center = lidar[2]
        right = (lidar[3] + lidar[4]) / 2

        # cooldown służy temu, żeby przeciwnik nie zachowywał się dziwnie przy ścianach
        if self.close_wall_check_cooldown < 0:
            # wpierw następuje sprawdzenie czy samochów nie jest zbyt blisko ściany
            # jeżeli jest to próbuje jechać w innym kierunku
            if right < 50:
                self.turn_left()
                self.close_wall_check_cooldown = 10
            elif left < 50:
                self.turn_right()
                self.close_wall_check_cooldown = 10

            # potem stara się jechać w stronę po której jest najwięcej miejsca
            # lewo, centrum albo prawo
            elif left > center and left > right:
                self.turn_left()

            elif right > left and right > center:
                self.turn_right()

                # jeżeli samochód nie skręcał w tej klatce to przyspiesza
            else:
                self.accelerate(1)
        else:
            self.accelerate(1)

        # zmniejszanie cooldownu reakcji na bliską ścianę
        self.close_wall_check_cooldown -= 1

    def draw_debug(self) -> None:
        super().draw_debug()
        # for p in lidar:
            # pygame.draw.line(self.game.screen, (255, 0, 0), tuple(self.position), tuple(p))


    def ray_march(self, start: Vector, direction: Vector) -> Vector:
        # wysyłanie promienia w wybranym kierunku i sprawdzenie
        # odległości od trafionego punktu
        # używamy metody podobnej do raymarchingu (ale jednak innej)
        # tu można poczytać więcej https://en.wikipedia.org/wiki/Ray_marching
        while self.game.map.is_point_on_track(start):
            # mnożymy razy pięć, żeby trochę to zoptymalizować
            # obliczenia są mniej precyzyjne, ale zajmują 5 razy mniej czasu
            start += direction * 5
        return start

class EnemyCar3(EnemyCar):
    def update(self) -> None:
        super().update()

        target = self.waypoints[self.next_target].position

        player = [car for car in self.game.cars if isinstance(car, PlayerCar)][0]
        to_player_vector = player.position - self.position
        try_to_hit_player = False
        if player.velocity.length() > 3:
            if to_player_vector.length() < 200 and self.direction_vector.scalar_product(player) > 0:
                try_to_hit_player = True
            elif to_player_vector.length() < 50:
                try_to_hit_player = True

        if try_to_hit_player:
            possible_position = player.position + player.direction_vector.rotate(math.pi / 2) * 40
            if self.map.is_point_on_track(possible_position):
                target = possible_position

        self.turn_to_target(target)

        target = self.waypoints[self.next_target]


    def draw(self) -> None:
        super().draw()


class EnemyCar4(EnemyCar2):
    def update(self) -> None:
        player = filter(lambda x: isinstance(x, PlayerCar), self.game.cars).__iter__().__next__()
        # naszym celem jest punkt przed graczem
        target = player.position + player.direction_vector * 100

        player_dist = (self.position - player.position).length()
        target_dist = (self.position - target).length()
        # jeżeli blisko gracza
        if player_dist < 250 and player.velocity.length() > 3:
            EnemyCar.update(self)
            # jeżeli bardziej przed graczem to ustaw się centralnie przed graczem
            if target_dist < player_dist:
                self.turn_to_target(target)
            # jeżeli bardziej za graczem to spróbuj wyprzedzić gracza
            else:
                target = player.position + player.direction_vector.rotate(math.pi/4) * 80
                self.turn_to_target(target)
            # pygame.draw.circle(self.game.screen, pygame.Color('red'), tuple(target), 3)
        # jeżeli daleko od gracza to jedź normalnie
        else:
            super().update()

    def draw(self) -> None:
        super().draw()
        # super().draw_debug()
