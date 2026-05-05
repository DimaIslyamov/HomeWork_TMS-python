import string
from enum import Enum


class Mode(Enum):
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"


def vigenere_cipher(text: str, key: str, mode: Mode) -> str:
    alphabet = string.ascii_lowercase
    n = len(alphabet)

    # пред расчет сдвигов ключа (ускоряет работу)
    key_shifts = [alphabet.index(k.lower()) for k in key]

    result = []
    key_index = 0

    for char in text:
        is_upper = char.isupper()
        lower_char = char.lower()

        if lower_char in alphabet:
            shift = key_shifts[key_index % len(key_shifts)]

            if mode == Mode.DECRYPT:
                shift = -shift

            index = alphabet.index(lower_char)
            new_index = (index + shift) % n
            new_char = alphabet[new_index]

            result.append(new_char.upper() if is_upper else new_char)
            key_index += 1
        else:
            result.append(char)

    return "".join(result)


print(vigenere_cipher("Hello World!", "key", Mode.ENCRYPT))
print(vigenere_cipher("Rijvs Uyvjn!", "key", Mode.DECRYPT))