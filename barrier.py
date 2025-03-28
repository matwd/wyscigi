import pygame
from hitbox import RectangleHitbox


class GateState:
    closing = 1
    waiting = 2
    opening = 3


class Barrier:
    def __init__(self, x, y, scale, is_dark=False):
        self.sprites = [pygame.image.load(f"assets/barrier/{i:>04}.png") for i in range(1, 17)]
        if is_dark:
            [s.fill((50, 50, 50), special_flags=pygame.BLEND_MULT) for s in self.sprites]
        self.sprites = [pygame.transform.scale(spr, (32 * scale, 512 * scale)).convert_alpha() for spr in self.sprites]
        self.pos = (x, y)
        self.frame = 0
        self.state = GateState.waiting
        self.wait_time = 60 * 10  # 10 sekund
        self.drawing_x = self.pos[0] - 16 * scale
        self.drawing_y = self.pos[1] - 256 * scale
        # wartości poniżej zależą od wielkości tekstury i umiejscowienia obiektów na teksturze
        self.hitbox = RectangleHitbox(x, y + 75 * scale, 0, 60 * scale, 128 * scale)

    def update(self):
        match self.state:
            case GateState.closing:
                self.frame -= 1
                if self.frame == 0:
                    self.state = GateState.waiting
                    self.wait_time = 60 * 10  # 10 sekund
            case GateState.opening:
                self.frame += 1
                if self.frame == 15:
                    self.state = GateState.waiting
                    self.wait_time = 60 * 5  # 5 sekund
            case GateState.waiting:
                if self.wait_time == 0:
                    self.state = GateState.opening if self.frame == 0 else GateState.closing
                else:
                    self.wait_time -= 1

    def draw(self, screen):
        screen.blit(self.sprites[self.frame], (self.drawing_x, self.drawing_y))

    def check_hit(self, point):
        """Sprawdzanie kolizji z szlabanem"""
        # nie można wjechać w szlaban, jeżeli jest on podniesiony
        if self.frame > 0:
            return False
        # w przeciwnym wypadku sprawdź normalne kolizje
        return self.hitbox.check_hit(point)
