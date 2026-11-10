"""Повышенное №7: хранение записей SQLite."""

from contextlib import closing
from pathlib import Path
import sqlite3


class Catalog:
    def __init__(self, path: Path) -> None:
        self.path = path
        with closing(sqlite3.connect(path)) as db, db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS items "
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)"
            )

    def items(self) -> list[tuple[int, str]]:
        with closing(sqlite3.connect(self.path)) as db:
            return db.execute("SELECT id, name FROM items ORDER BY id").fetchall()

    def add(self, name: str) -> None:
        name = name.strip()
        if not name:
            raise ValueError("Введите название")
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute("INSERT INTO items (name) VALUES (?)", (name,))

    def delete(self, item_id: int) -> None:
        with closing(sqlite3.connect(self.path)) as db, db:
            db.execute("DELETE FROM items WHERE id = ?", (item_id,))
