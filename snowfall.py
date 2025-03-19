from random import randrange, random, randint

import pygame.image
import os

from pygame.math import clamp


class Snowflake:
    """
    Klasa bez funkcji, jedynie służąca do przechowywania informacji o pojedyńczej śnieżce.
    Ma parametry wind i fall, takie same jak w klasie głównej, pozwalając na trochę inny tor od głównego.
    Zawsze zaczyna ponad ekranem.
    """
    def __init__(self, image: pygame.Surface, wind: float, fall: float, x: float):
        self.x = x
        self.y = -image.get_height()
        self.wind = wind
        self.fall = fall
        self.image = image

class Snowfall:
    """
    Klasa odpowiadająca za kontrolę śniegu. Dostępne parametry:

    wind (wiatr) - jak bardzo i w którą stronę lecą śnieżki (prawo/lewo)
    fall (spadek) - szybkość spadania śnieżek, musi być większa od 0
    density (gęstość) - jak dużo śnieżek jest tworzonych co klatkę. Musi być większa od 0 żeby pojawiły się jakiekolwiek śnieżki. jeżeli jest mniejsza od 1 to pojawiają się co kilka klatek.
    diversity (odmienność) - jak bardzo może się różnić tor pojedyńczej śnieżki wzgledem głównego.
    width (szerokość) - szerokość ekranu
    height (wysokość) - wysokość ekranu
    """

    def __init__(self, wind: float, fall: float, density: float, diversity: float, width: float, height: float):
        self.wind = wind
        self.fall = fall
        self.width = width
        self.height = height
        self.diversity = diversity
        self.density = density
        self.images = [
            pygame.image.load("./assets/snowfall/" + file)
            for file in os.listdir("./assets/snowfall")
            if os.path.isfile("./assets/snowfall/" + file)
        ]
        self.snowflakes = []

    def snowfall(self, screen: pygame.Surface, wind_change: float):
        for (i, snowflake) in enumerate(self.snowflakes):
            snowflake.y += snowflake.fall
            if (snowflake.y > self.height or
                    (self.wind < 0 and snowflake.x < -snowflake.image.get_width()) or
                    (self.wind > 0 and snowflake.x > self.width + snowflake.image.get_width())):
                # self.snowflakes.remove(snowflake)
                del self.snowflakes[i]
            else:
                snowflake.x += snowflake.wind + self.wind
                snowflake.wind = clamp(snowflake.wind + random() - 0.5, -self.diversity, self.diversity)
                screen.blit(snowflake.image, (snowflake.x, snowflake.y), snowflake.image.get_rect())
        offset = self.wind * self.height / self.fall
        if self.density >= 1:
            self.snowflakes.extend([
                Snowflake(
                    self.images[randrange(0, len(self.images))],
                    (random() - 0.5) * self.diversity,
                    self.fall + random() * self.diversity,
                    random() * (self.width + abs(offset)) - (offset if self.wind > 0 else 0)
                )
                for _ in range(randint(0, int(self.density + random())))
            ])
        elif random() < self.density:
            self.snowflakes.append(
                Snowflake(
                    self.images[randrange(0, len(self.images))],
                    (random() - 0.5) * self.diversity,
                self.fall + random() * self.diversity, random() * (self.width + abs(offset)) - (offset if self.wind > 0 else 0)
            ))
