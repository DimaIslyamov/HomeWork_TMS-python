# # ==== мой вариант который не очень =====
# # === Шифровка ===
# def encrypt(message: str, shift: int = 3) -> str:
#     alphabet: str = "abcdefghijklmnopqrstuvwxyz"
#     result: str = ""
#
#     for char in message:
#         if char in alphabet:
#             index = alphabet.index(char)
#             new_index = (index + shift) % 26
#             result += alphabet[new_index]
#         else:
#             result += char
#
#     return result
#
#
# # === Дешифровка ===
# def decrypt(message: str, shift: int = 3) -> str:
#     return encrypt(message, -shift)
#
#
# user_choice: str = input("Введите что вы хотите 'encrypt' или 'decrypt': ").lower()
# user_str: str = input("Введите слово на английском: ").lower()
#
# if user_choice == "encrypt":
#     print(encrypt(user_str))
# elif user_choice == "decrypt":
#     print(decrypt(user_str))
# else:
#     print("Неверно было введено слово 'encrypt' или 'decrypt'")


# ==== Старый код для vigenere ====
# def encrypt_vigenere(massage: str, key: str) -> str:
#     alphabet: str = "abcdefghijklmnopqrstuvwxyz"
#     result: str = ""
#     key_index: int = 0 # отдельный индекс ключа
#
#     for i in range(len(massage)):
#         char = massage[i]  # Берём букву сообщения
#
#         if char in alphabet:
#             key_char = key[key_index % len(key)]  # Берём букву ключа
#                                             # Ключ зацикливается
#             index = alphabet.index(char)
#             shift = alphabet.index(key_char)  # получаем сдвиг
#
#             new_index = (index + shift) % 26  # шифруем
#             result += alphabet[new_index]
#
#             key_index += 1 # Двигаем только на буквах
#         else:
#             result += char
#
#     return result
#
#
# def decrypt_vigenere(massage: str, key: str) -> str:
#     alphabet: str = "abcdefghijklmnopqrstuvwxyz"
#     result: str = ""
#     key_index: int = 0
#
#     for i in range(len(massage)):
#         char = massage[i]
#
#         if char in alphabet:
#             key_char = key[key_index % len(key)]
#
#             index = alphabet.index(char)
#             shift = alphabet.index(key_char)
#
#             new_index = (index - shift) % 26
#             result += alphabet[new_index]
#
#             key_index += 1
#         else:
#             result += char
#
#     return result
