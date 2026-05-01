def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b

    return a

user_a = int(input("Введите число А: "))
user_b = int(input("Введите число Б: "))

value = gcd(a=user_a, b=user_b)
print(value)