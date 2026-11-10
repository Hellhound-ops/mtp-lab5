"""ЛР №5, вариант 3: четыре вкладки Tkinter для пяти заданий."""

import argparse
from pathlib import Path
import sqlite3
import tkinter as tk
from itertools import cycle
from tkinter import messagebox, ttk

from calculator import OPERATIONS, calculate
from catalog import Catalog


def calculator_tab(parent: ttk.Frame) -> None:
    left = ttk.Entry(parent, width=18)
    operator = ttk.Combobox(parent, values=tuple(OPERATIONS), width=4, state="readonly")
    operator.current(0)
    right = ttk.Entry(parent, width=18)
    result = ttk.Label(parent, text="Введите два числа")

    def show_result() -> None:
        try:
            value = calculate(left.get(), operator.get(), right.get())
            result.config(text=f"Результат: {value}")
        except ValueError as error:
            result.config(text=str(error))

    ttk.Label(parent, text="Первое число").grid(row=0, column=0, sticky="w")
    ttk.Label(parent, text="Второе число").grid(row=0, column=2, sticky="w")
    left.grid(row=1, column=0, pady=6)
    operator.grid(row=1, column=1, padx=8)
    right.grid(row=1, column=2)
    ttk.Button(parent, text="Вычислить", command=show_result).grid(row=2, column=0, sticky="w")
    result.grid(row=3, column=0, columnspan=3, sticky="w", pady=8)


def color_tab(parent: ttk.Frame) -> None:
    colors = cycle(("#285078", "#a3492c", "#327356"))
    color = next(colors)
    panel = tk.Frame(parent, background=color, height=140)
    label = ttk.Label(parent, text=color)

    def change_color() -> None:
        selected = next(colors)
        panel.config(background=selected)
        label.config(text=selected)

    panel.pack(fill="x", pady=(0, 8))
    label.pack(anchor="w")
    ttk.Button(parent, text="Сменить цвет", command=change_color).pack(anchor="w", pady=8)


def clicker_tab(parent: ttk.Frame) -> None:
    score = tk.IntVar(parent, value=0)
    ttk.Label(parent, text="Количество нажатий").pack(anchor="w")
    ttk.Label(parent, textvariable=score, font=("Segoe UI", 24)).pack(anchor="w")
    ttk.Button(parent, text="Нажать", command=lambda: score.set(score.get() + 1)).pack(anchor="w")
    ttk.Button(parent, text="Сбросить", command=lambda: score.set(0)).pack(anchor="w", pady=8)


def catalog_tab(parent: ttk.Frame, catalog: Catalog) -> None:
    ttk.Label(parent, text="Название записи").pack(anchor="w")
    name = ttk.Entry(parent)
    name.pack(fill="x", pady=(4, 8))
    buttons = ttk.Frame(parent)
    buttons.pack(fill="x")
    rows = ttk.Treeview(parent, columns=("id", "name"), show="headings", selectmode="browse")
    rows.heading("id", text="№")
    rows.heading("name", text="Название")
    rows.column("id", width=55, stretch=False)
    rows.pack(fill="both", expand=True, pady=(8, 0))

    def refresh() -> None:
        records = catalog.items()
        rows.delete(*rows.get_children())
        for item_id, item_name in records:
            rows.insert("", "end", iid=str(item_id), values=(item_id, item_name))

    def add_item() -> None:
        try:
            catalog.add(name.get())
            name.delete(0, "end")
            refresh()
        except (ValueError, sqlite3.Error) as error:
            messagebox.showerror("Каталог SQLite", str(error), parent=parent)

    def delete_item() -> None:
        selected = rows.selection()
        if selected:
            try:
                catalog.delete(int(selected[0]))
                refresh()
            except sqlite3.Error as error:
                messagebox.showerror("Каталог SQLite", str(error), parent=parent)

    ttk.Button(buttons, text="Добавить", command=add_item).pack(side="left")
    ttk.Button(buttons, text="Удалить выбранную", command=delete_item).pack(side="left", padx=8)
    refresh()


def build_window(root: tk.Tk, catalog: Catalog) -> ttk.Notebook:
    root.title("МТП · Лабораторная №5 · Вариант 3")
    root.minsize(560, 360)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=12, pady=12)
    for title, build in (
        ("Калькулятор", calculator_tab),
        ("Цветная панель", color_tab),
        ("Кликер", clicker_tab),
        ("Каталог SQLite", lambda frame: catalog_tab(frame, catalog)),
    ):
        frame = ttk.Frame(notebook, padding=12)
        notebook.add(frame, text=title)
        build(frame)
    return notebook


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path("lab5.sqlite3"), help="файл каталога")
    args = parser.parse_args()
    try:
        catalog = Catalog(args.db)
        root = tk.Tk()
        build_window(root, catalog)
    except (sqlite3.Error, tk.TclError) as error:
        parser.exit(1, f"Ошибка запуска: {error}\n")
    root.mainloop()


if __name__ == "__main__":
    main()
