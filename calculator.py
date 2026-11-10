"""Среднее №3: операции калькулятора."""

from decimal import Decimal, DecimalException
from operator import add, mul, sub, truediv


OPERATIONS = {"+": add, "−": sub, "×": mul, "÷": truediv}


def calculate(left: str, symbol: str, right: str) -> Decimal:
    """Вычислить результат для двух конечных десятичных чисел."""
    operation = OPERATIONS.get(symbol)
    if operation is None:
        raise ValueError("Выберите арифметическую операцию")
    try:
        first = Decimal(left.strip().replace(",", "."))
        second = Decimal(right.strip().replace(",", "."))
    except DecimalException as error:
        raise ValueError("Введите два числа") from error

    if not first.is_finite() or not second.is_finite():
        raise ValueError("Введите конечные числа")
    if symbol == "÷" and second == 0:
        raise ValueError("Деление на ноль")
    try:
        return operation(first, second)
    except DecimalException as error:
        raise ValueError("Результат за пределами диапазона") from error
