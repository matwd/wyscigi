from vector import Vector
from hitbox import RectangleHitbox, CircleHitbox
import math
from pytest import approx


def test_vector_operations():
    vector = Vector(4,3)

    assert vector.length()==5
    assert vector == Vector(4,3)
    assert -vector == Vector(-4,-3)
    assert vector+Vector(6,7) == Vector(approx(10),approx(10))
    assert vector-Vector(2,1) == Vector(approx(2),approx(2))
    assert vector*3==Vector(approx(12),approx(9))
    assert vector/2==Vector(approx(2),approx(1.5))
    
def test_vector_methods():
    vector = Vector(4,3)

    assert vector.rotate(math.pi*2) == Vector(approx(4),approx(3))
    assert vector.rotate(math.pi) == Vector(approx(-4), approx(-3))
    assert vector.rotate(math.pi/2) == Vector(approx(-3), approx(4))
    assert vector.rotate(math.pi * 3 / 2) == Vector(approx(3), approx(-4))
    assert vector.scalar_product(Vector(5,6)) == approx(38)
    assert vector.normalize().length() == approx(1)

def test_rect_hitbox():
    rect = RectangleHitbox(500,500,0,100,100)

    assert rect.check_hit(Vector(475,475))
    assert rect.check_hit(Vector(200,200))!=True
    assert rect.check_hit(Vector(530,530))
    assert rect.check_hit(Vector(510,490))

    rect_points = rect.get_points()

    assert rect_points[0] == Vector(approx(550),approx(450))
    assert rect_points[1] == Vector(approx(550),approx(550))
    assert rect_points[2] == Vector(approx(450),approx(550))
    assert rect_points[3] == Vector(approx(450),approx(450))


    assert rect.get_points() == (Vector(approx(550),approx(450)),Vector(approx(550),approx(550)),Vector(approx(450),approx(550)),Vector(approx(450),approx(450)))

def test_circle_hitbox():
    circle = CircleHitbox(200,200,100)

    assert circle.check_hit(Vector(200,200))
    assert circle.check_hit(Vector(10,50))!=True
    assert circle.check_hit(Vector(200,110))
    assert circle.check_hit(Vector(150,220))