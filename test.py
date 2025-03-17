from vector import Vector
import math
from pytest import approx

def test_vector_methods():
    vector1 = Vector(4,3)

    assert vector1.length()==5
    assert vector1 == Vector(4,3)
    assert -vector1 == Vector(-4,-3)
    assert vector1+Vector(6,7) == Vector(approx(10),approx(10))
    assert vector1-Vector(2,1) == Vector(approx(2),approx(2))
    assert vector1*3==Vector(approx(12),approx(9))
    assert vector1/2==Vector(approx(2),approx(1.5))
    assert vector1.rotate(math.pi*2) == Vector(approx(4),approx(3))
    assert vector1.rotate(math.pi) == Vector(approx(-4), approx(-3))
    assert vector1.rotate(math.pi/2) == Vector(approx(-3), approx(4))
    assert vector1.rotate(math.pi * 3 / 2) == Vector(approx(3), approx(-4))
    assert vector1.scalar_product(Vector(5,6)) == approx(38)
    assert vector1.normalize().length() == approx(1)