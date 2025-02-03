class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        return self / self.length()

    def scalar_product(self, second):
        return self.x * second.y + self.y * second.y

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __rmul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __add__(self, second):
        return Vector(self.x + second.x, self.y + second.y)

    def __sub__(self, second):
        return Vector(self.x - second.x, self.y - second.y)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __iter__(self):
        def iterator():
            yield self.x
            yield self.y

        return iterator()
