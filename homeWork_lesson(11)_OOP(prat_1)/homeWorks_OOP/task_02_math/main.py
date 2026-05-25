class Math:
    @staticmethod
    def addition(a, b):
        print(a + b)

    @staticmethod
    def subtraction(a, b):
        print(a - b)

    @staticmethod
    def multiplication(a, b):
        print(a * b)

    @staticmethod
    def division(a, b):
        try:
            print(a / b)
        except ZeroDivisionError:
            print("На ноль делить нельзя")


if __name__ == "__main__":
    math_obj = Math()

    math_obj.addition(4, 5)
    math_obj.subtraction(4, 5)
    math_obj.multiplication(4, 5)
    math_obj.division(4, 5)
