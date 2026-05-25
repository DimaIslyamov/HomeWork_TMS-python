from math import pi


class Sphere:
    def __init__(self, radius=1, x=0, y=0, z=0):
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z

    def get_volume(self):
        return 4 / 3 * pi * self.radius ** 3

    def get_square(self):
        return 4 * pi * self.radius ** 2

    def get_radius(self):
        return self.radius

    def get_center(self):
        return self.x, self.y, self.z

    def set_radius(self, radius):
        self.radius = radius

    def set_center(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def is_point_inside(self, x, y, z):
        return (
                (x - self.x) ** 2
                + (y - self.y) ** 2
                + (z - self.z) ** 2
                <= self.radius ** 2
        )


if __name__ == "__main__":
    sphere_1 = Sphere()

    print("Проверка sphere_1")
    print("Радиус:", sphere_1.get_radius())
    print("Центр:", sphere_1.get_center())
    print("Объём:", round(sphere_1.get_volume(), 2))
    print("Площадь:", round(sphere_1.get_square(), 2))
    print("Точка (0, 0, 0) внутри:", sphere_1.is_point_inside(0, 0, 0))
    print("Точка (2, 0, 0) внутри:", sphere_1.is_point_inside(2, 0, 0))

    print()

    print("Проверка изменения radius и center")
    sphere_2 = Sphere(3, 1, 2, 3)

    sphere_2.set_radius(10)
    sphere_2.set_center(0, 0, 0)

    print("Новый радиус:", sphere_2.get_radius())
    print("Новый центр:", sphere_2.get_center())
    print("Новый объём:", round(sphere_2.get_volume(), 2))
    print("Новая площадь:", round(sphere_2.get_square(), 2))
    print("Точка (9, 0, 0) внутри:", sphere_2.is_point_inside(9, 0, 0))
    print("Точка (11, 0, 0) внутри:", sphere_2.is_point_inside(11, 0, 0))
