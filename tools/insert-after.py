#!/usr/bin/env python3
"""
Вставляет после уникальной строки (якоря) блок:
    (пустая строка)
    <!-- вставка стилей выпадающей панели -->
    <link rel="stylesheet" href="assets/css/panel.css">

Идемпотентен: если блок уже стоит после якоря — файл пропускается.

Использование:
    python3 insert-after.py

Настройки — в блоке CONFIG ниже.
"""

import os
import sys

# ==================== CONFIG ====================
ANCHOR_LINE = '<link rel="stylesheet" href="assets/css/style-main.css">'

# Что вставляем ПОСЛЕ якоря (по порядку, каждая строка отдельно):
INSERT_LINES = [
    "",  # пустая строка перед комментарием
    "<!-- вставка стилей выпадающей панели -->",
    '<link rel="stylesheet" href="assets/css/panel.css">',
    "",  # пустая строка после блока ← добавили
]

# Маркер для проверки идемпотентности (строка, по которой узнаём,
# что блок уже вставлен). Обычно это комментарий из INSERT_LINES.
MARKER = "<!-- вставка стилей выпадающей панели -->"
# ================================================

ROOT = "."
SKIP_DIRS = {".git", "node_modules", "assets", "pictures", ".github"}


def process_file(path: str) -> str:
    """Возвращает статус: 'inserted', 'skipped', 'no-anchor'."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Ищем якорь (первое вхождение)
    idx = None
    for i, line in enumerate(lines):
        if ANCHOR_LINE in line:
            idx = i
            break

    if idx is None:
        return "no-anchor"

    # Проверяем, есть ли уже блок после якоря.
    # Смотрим несколько строк вперёд (пропуская пустые) на MARKER.
    j = idx + 1
    found_marker = False
    while j < len(lines) and j <= idx + 5:  # смотрим не дальше 5 строк
        if MARKER in lines[j]:
            found_marker = True
            break
        if lines[j].strip() != "":
            # первая непустая строка после якоря — если это не MARKER,
            # значит блока нет (или он в другом месте)
            break
        j += 1

    if found_marker:
        return "skipped"

    # Вставляем блок ПОСЛЕ якоря.
    # Отступ берём от якорной строки (чтобы вставка была выровнена).
    indent = lines[idx][:len(lines[idx]) - len(lines[idx].lstrip())]

    insert_pos = idx + 1
    for i, raw in enumerate(INSERT_LINES):
        if raw == "":
            new_line = "\n"
        else:
            new_line = indent + raw.strip() + "\n"
        lines.insert(insert_pos + i, new_line)

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return "inserted"


def main():
    counters = {"inserted": 0, "skipped": 0, "no-anchor": 0}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for name in filenames:
            if not name.lower().endswith((".html", ".htm")):
                continue
            path = os.path.join(dirpath, name)
            try:
                status = process_file(path)
            except Exception as e:
                print(f"[ERROR] {path}: {e}")
                continue
            counters[status] += 1
            print(f"[{status.upper():9}] {path}")

    print("\nИтого:")
    print(f"  вставлено:       {counters['inserted']}")
    print(f"  пропущено (уже): {counters['skipped']}")
    print(f"  без якоря:       {counters['no-anchor']}")


if __name__ == "__main__":
    sys.exit(main())
