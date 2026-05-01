def is_prime(n) -> bool:
    if n <= 1:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False

    return True


prime = int(input("Введите число: "))

if is_prime(n=prime):
    print(f"Число {prime} простое")
else:
    print(f"Число {prime} не простое")
