user_input_str = input("Введите строку: ")

# Третий символ этой строки.
print(user_input_str[2])

# Предпоследний символ строки.
print(user_input_str[-2])

# Первые пять символов строки.
print(user_input_str[:5])

# Вся до последних двух символов.
print(user_input_str[:-2])

# С четными индексами, начиная с первого
print(user_input_str[::2])

# С нечетными индексами, начиная со второго символа строки.
print(user_input_str[1::2])

# В обратном порядке.
print(user_input_str[::-1])

# В обратном порядке, начиная с последнего.
print(user_input_str[::-2])

# Длина строки
print(len(user_input_str))