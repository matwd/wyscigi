from vector import Vector
import pygame

class RectangleHitbox:
    def __init__(self, x, y, rotation, width, height):
        self.pos = Vector(x, y)
        self.rotation = rotation
        self.width = width
        self.height = height

    def get_points(self):
        point1_offset = Vector(self.width/2, -self.height/2).rotate(self.rotation)
        point2_offset = Vector(self.width/2, self.height/2).rotate(self.rotation)
        point3_offset = -point1_offset
        point4_offset = -point2_offset

        point1 = point1_offset + self.pos
        point2 = point2_offset + self.pos
        point3 = point3_offset + self.pos
        point4 = point4_offset + self.pos

        return (point1, point2, point3, point4)

    def draw(self, screen):
        points = self.get_points()

        pygame.draw.circle(screen, (100, 0, 0), tuple(points[0]), 3)
        pygame.draw.circle(screen, (150, 0, 0), tuple(points[1]), 3)
        pygame.draw.circle(screen, (200, 0, 0), tuple(points[2]), 3)
        pygame.draw.circle(screen, (250, 0, 0), tuple(points[3]), 3)

        pygame.draw.line(screen, (255, 0, 0), tuple(points[0]), tuple(points[1]), 3)
        pygame.draw.line(screen, (255, 0, 0), tuple(points[1]), tuple(points[2]), 3)
        pygame.draw.line(screen, (255, 0, 0), tuple(points[2]), tuple(points[3]), 3)
        pygame.draw.line(screen, (255, 0, 0), tuple(points[3]), tuple(points[0]), 3)

    def check_hit(self, screen, point):
        relative_vector = self.pos - point
        relative_vector.rotate(-self.rotation)
        if abs(relative_vector.x) < self.width / 2 and abs(relative_vector.y) < self.height / 2:
            return True

