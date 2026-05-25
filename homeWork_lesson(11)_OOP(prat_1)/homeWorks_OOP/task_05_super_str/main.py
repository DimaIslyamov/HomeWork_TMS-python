class SuperStr(str):
    def is_repeatance(self, s: str) -> bool:
        if not self or not s:
            return False

        if len(self) % len(s) != 0:
            return False

        count = len(self) // len(s)

        return self == s * count

    def is_palindrome(self) -> bool:
        text = self.lower()
        return text == text[::-1]


if __name__ == "__main__":
    print(SuperStr("abcabcabc").is_repeatance("abc"))
    print(SuperStr("abcabcab").is_repeatance("abc"))

    print()

    print(SuperStr("казак").is_palindrome())
    print(SuperStr("hello").is_palindrome())
    print(SuperStr("").is_palindrome())
