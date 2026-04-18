n = int(input("Сумма телефона: "))
k = int(input("Какую сумму вы можете откладывать за день: "))

total: int = 0
days: int = 0

while total < n:
    days += 1

    if days % 7 != 0:
        total += k

print(days)
