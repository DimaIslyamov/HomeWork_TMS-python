# === Шифровка ===
def encrypt(message: str, shift: int = 3) -> str:
    alphabet: str = "abcdefghijklmnopqrstuvwxyz"
    result: str = ""

    for char in message:
        if char in alphabet:
            index = alphabet.index(char)
            new_index = (index + shift) % 26
            result += alphabet[new_index]
        else:
            result += char

    return result


# === Дешифровка ===
def decrypt(message: str, shift: int = 3) -> str:
    return encrypt(message, -shift)


user_choice: str = input("Введите что вы хотите 'encrypt' или 'decrypt': ").lower()
user_str: str = input("Введите слово на английском: ").lower()

if user_choice == "encrypt":
    print(encrypt(user_str))
elif user_choice == "decrypt":
    print(decrypt(user_str))
else:
    print("Неверно было введено слово 'encrypt' или 'decrypt'")
