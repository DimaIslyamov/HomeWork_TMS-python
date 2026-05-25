class Car:
    def __init__(self, car_color, car_type, car_year):
        self.car_color = car_color
        self.car_type = car_type
        self.car_year = car_year

    @staticmethod
    def start_auto():
        print("Автомобиль заведён")

    @staticmethod
    def stop_auto():
        print("Автомобиль заглушен")

    def set_auto_year(self, car_year):
        self.car_year = car_year

    def set_auto_type(self, car_type):
        self.car_type = car_type

    def set_auto_color(self, car_color):
        self.car_color = car_color


if __name__ == "__main__":
    car = Car("black", "sedan", 2020)

    car.start_auto()
    car.stop_auto()

    car.set_auto_color("красная")
    car.set_auto_type("купе")
    car.set_auto_year(2023)

    print(f"Ваша машина цвета {car.car_color.title()}"
          f" в кузове {car.car_type.title()}"
          f" сделана в {car.car_year}г.")
