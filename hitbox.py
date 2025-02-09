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

        pygame.draw.circle(screen, (100, 0, 0), tuple(points[0]), 2)
        pygame.draw.circle(screen, (150, 0, 0), tuple(points[1]), 2)
        pygame.draw.circle(screen, (200, 0, 0), tuple(points[2]), 2)
        pygame.draw.circle(screen, (250, 0, 0), tuple(points[3]), 2)

