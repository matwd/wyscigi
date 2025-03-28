from vector import Vector
import pygame

class Hitbox:
    """
    Klasa abstrakcyjna dla hitboxów w różnych kształtach
    """
    def __init__(self) -> None:
        raise NotImplementedError("Nie zaimplementowano inicjalizacji wektora")

    def draw(self, screen: pygame.surface.Surface) -> None:
        "Rysowanie hitboxa (dla debugowania/nie powinno być użyte w grze)"
        raise NotImplementedError("Nie zaimplementowano rysowania hitboxa")

    def check_hit(self, point: Vector) -> bool:
        "Sprawdzanie kolizji punktu z hitboxem"
        raise NotImplementedError("Nie zaimplementowano sprawdzania przynależności punktu do hitboxa")

class CircleHitbox(Hitbox):
    def __init__(self, x: int, y: int, radius: int):
        self.position = Vector(x, y)
        self.radius = radius

    def draw(self, screen: pygame.surface.Surface) -> None:
        pygame.draw.circle(screen, (255, 0, 0, 0), tuple(self.position), self.radius)

    def check_hit(self, point: Vector) -> bool:
        return (self.position - point).length() < self.radius

class RectangleHitbox(Hitbox):
    """
    Hitbox w kształci prostokąta
    Prostokąt może być obrócony (parametr rotation)
    """
    def __init__(self, x: int, y: int, rotation: int, width: int, height: int) -> None:
        self.position = Vector(x, y)
        self.rotation = rotation
        self.width = width
        self.height = height

    def get_points(self) -> tuple[Vector, Vector, Vector, Vector]:
        "Zwraca listę krawędzi prostokąta"
        point1_offset = Vector(self.width/2, -self.height/2).rotate(self.rotation)
        point2_offset = Vector(self.width/2, self.height/2).rotate(self.rotation)
        point3_offset = -point1_offset
        point4_offset = -point2_offset

        point1 = point1_offset + self.position
        point2 = point2_offset + self.position
        point3 = point3_offset + self.position
        point4 = point4_offset + self.position

        return (point1, point2, point3, point4)

    def draw(self, screen: pygame.surface.Surface) -> None:
        points = self.get_points()

        pygame.draw.circle(screen, (100, 0, 0), tuple(points[0]), 3)
        pygame.draw.circle(screen, (150, 0, 0), tuple(points[1]), 3)
        pygame.draw.circle(screen, (200, 0, 0), tuple(points[2]), 3)
        pygame.draw.circle(screen, (250, 0, 0), tuple(points[3]), 3)

        pygame.draw.line(screen, (255, 0, 0), tuple(points[0]), tuple(points[1]), 3)
        pygame.draw.line(screen, (255, 0, 0), tuple(points[1]), tuple(points[2]), 3)
        pygame.draw.line(screen, (255, 0, 0), tuple(points[2]), tuple(points[3]), 3)
        pygame.draw.line(screen, (255, 0, 0), tuple(points[3]), tuple(points[0]), 3)

    def check_hit(self, point: Vector) -> bool:
        relative_vector = self.position - point
        relative_vector.rotate(-self.rotation)
        if abs(relative_vector.x) < self.width / 2 and abs(relative_vector.y) < self.height / 2:
            return True

