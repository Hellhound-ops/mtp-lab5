"""Проверки расчётов и сохранения записей между запусками."""

from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from calculator import calculate
from catalog import Catalog


class CalculatorTests(unittest.TestCase):
    def test_operations(self):
        for symbol, expected in (("+", "8"), ("−", "4"), ("×", "12"), ("÷", "3")):
            with self.subTest(symbol=symbol):
                self.assertEqual(calculate("6", symbol, "2"), Decimal(expected))
        self.assertEqual(calculate("0,1", "+", "0.2"), Decimal("0.3"))

    def test_bad_input(self):
        for left, symbol, right in (("текст", "+", "1"), ("NaN", "+", "1"), ("1", "÷", "0")):
            with self.subTest(left=left, symbol=symbol, right=right):
                with self.assertRaises(ValueError):
                    calculate(left, symbol, right)


class CatalogTests(unittest.TestCase):
    def test_round_trip(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.sqlite3"
            Catalog(path).add(" Учебник 'Python' ")
            catalog = Catalog(path)
            item_id, name = catalog.items()[0]
            self.assertEqual(name, "Учебник 'Python'")
            with self.assertRaises(ValueError):
                catalog.add("  ")
            catalog.delete(item_id)
            self.assertEqual(Catalog(path).items(), [])
