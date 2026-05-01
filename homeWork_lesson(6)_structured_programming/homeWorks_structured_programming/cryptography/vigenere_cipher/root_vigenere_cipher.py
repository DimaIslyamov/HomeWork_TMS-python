from homeWorks_structured_programming.cryptography.vigenere_cipher.vigenere_cipher import encrypt_vigenere, decrypt_vigenere


# === Ввод пользователя ===
user_choice = input("Введите 'encrypt' или 'decrypt': ").lower()
user_message = input("Введите сообщение: ").lower()
key = input("Введите ключ (слово): ").lower()

if not key.isalpha():
    print("Ключ должен содержать только буквы!")
else:
    if user_choice == "encrypt":
        print("Результат:", encrypt_vigenere(user_message, key))
    elif user_choice == "decrypt":
        print("Результат:", decrypt_vigenere(user_message, key))
    else:
        print("Неверный выбор")
