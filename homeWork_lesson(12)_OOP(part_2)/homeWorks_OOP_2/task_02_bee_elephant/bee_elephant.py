from dataclasses import dataclass


@dataclass
class BeeElephant:
    _bee_part: int
    _elephant_part: int

    @property
    def bee_part(self) -> int:
        return self._bee_part

    @property
    def elephant_part(self) -> int:
        return self._elephant_part

    # ===== Методы с задания =====
    def fly(self) -> bool:
        return self.bee_part >= self.elephant_part

    def trumpet(self) -> str:
        if self.elephant_part >= self.bee_part:
            return "tu-tu-doo-doo"
        return "wzzzz"

    def eat(self, meal: str, value: int) -> None:
        if value < 0:
            raise ValueError("Количество еды не может быть отрицательным")

        if meal == 'nectar':
            self._elephant_part -= value
            self._bee_part += value
        elif meal == 'grass':
            self._bee_part -= value
            self._elephant_part += value
        else:
            raise ValueError("Еда должна быть 'nectar' или 'grass'")

        self._normalize_parts()

    def _normalize_parts(self) -> None:
        self._bee_part = max(0, min(100, self._bee_part))
        self._elephant_part = max(0, min(100, self._elephant_part))
