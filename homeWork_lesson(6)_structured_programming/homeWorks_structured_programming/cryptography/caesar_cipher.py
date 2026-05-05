import string
from enum import Enum


class Mode(Enum):
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"


class Language(Enum):
    EN = "en"
    RU = "ru"


def cezar_cipher(text: str, shift: int, mode: Mode, language: Language) -> str:
    # Определение Алфавита
    if language == Language.EN:
        alphabet = string.ascii_lowercase
    elif language == Language.RU:
        alphabet = "abcdefghijklmnopqrstuvwxyz"
    else:
        raise ValueError(f"{language} is not supported")

    # Обработка режима
    if mode == Mode.ENCRYPT:
        actual_shift = shift
    elif mode == Mode.DECRYPT:
        actual_shift = -shift
    else:
        raise ValueError(f"{mode} is not supported")

    n = len(alphabet)
    result: list[str] = []

    for char in text:
        is_upper = char.isupper()
        lower_char = char.lower()

        if lower_char in alphabet:
            index = alphabet.find(lower_char)
            new_index = (index + actual_shift) % n
            new_char = alphabet[new_index]
            result.append(new_char.upper() if is_upper else  new_char)
        else:
            result.append(char)

    return "".join(result)


print(cezar_cipher(text="Hello World!", shift=3, mode=Mode.ENCRYPT, language=Language.EN))
print(cezar_cipher(text="Khoor Zruog!", shift=3, mode=Mode.DECRYPT, language=Language.EN))
