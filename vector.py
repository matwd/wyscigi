import math

class Vector:
    """
    Klasa wektoru.
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def length(self):
        """
        Zwraca długość wektoru
        """
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        """
        Zwraca wektor o tym samym zwrocie, ale długości 1
        """
        return self / self.length()

    def scalar_product(self, second):
        """
        Zwraca iloczyn skalarny dwóch wektorów
        """
        return self.x * second.x + self.y * second.y

    def __mul__(self, scalar):
        """
        Zwraca wektor pomnożony przez skalar
        """
        return Vector(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        """
        Zwraca wektor podzielony przez skalar
        """
        return Vector(self.x / scalar, self.y / scalar)

    def __truediv__(self, scalar):
        """
        Zwraca wektor podzielony przez skalar
        """
        return Vector(self.x / scalar, self.y / scalar)

    def __rmul__(self, scalar):
        """
        Zwraca wektor pomnożony przez skalar
        """
        return Vector(self.x * scalar, self.y * scalar)

    def __add__(self, second):
        """
        Zwraca sumę wektorów
        """
        return Vector(self.x + second.x, self.y + second.y)

    def __sub__(self, second):
        """
        Zwraca różnicę wektorów
        """
        return Vector(self.x - second.x, self.y - second.y)

    def __neg__(self):
        """
        Zwraca odwrotny wektor
        """
        return Vector(-self.x, -self.y)

    def __str__(self):
        """
        Zwraca informacje o wektorze w formie tekstowej
        """
        return f"Vector({self.x}, {self.y})"

    def __iter__(self):
        def iterator():
            yield self.x
            yield self.y

        return iterator()

    def __eq__(self, second):
        """
        Porównuje 2 wektory
        """
        return self.x==second.x and self.y==second.y

    def rotate(self, rotation):
        # obrot w radianach
        """
        Obrócenie wektora wokół punktu zaczepienia
        """
        s, c = math.sin(rotation), math.cos(rotation)
        return Vector(c * self.x - s * self.y, c * self.y + s * self.x)

    def copy(self):
        return Vector(self.x, self.y)

