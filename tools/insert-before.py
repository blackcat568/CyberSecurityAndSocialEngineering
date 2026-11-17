#!/usr/bin/env python3
"""
Вставляет заданный текст перед уникальной строкой во всех .html файлах.
Идемпотентен: если текст уже стоит перед строкой — файл пропускается.

Использование:
    python3 insert-before.py

Настройки — в блоке CONFIG ниже.
"""

import os
import sys

# ==================== CONFIG ====================
UNIQUE_LINE = '<script src="assets/js/articles-list.js"></script>'
INSERT_TEXT  = '<!-- подключение скриптов панели статей -->'
# ================================================

# Корень, откуда искать .html (текущая папка по умолчанию)
ROOT = "."

# Папки, которые не трогаем
SKIP_DIRS = {".git", "node_modules", "assets", "pictures", ".github"}

def process_file(path: str) -> str:
    """Возвращает статус: 'inserted', 'skipped', 'no-anchor'."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Ищем уникальную строку (первое вхождение)
    idx = None
    for i, line in enumerate(lines):
        if UNIQUE_LINE in line:
            idx = i
            break

    if idx is None:
        return "no-anchor"

    # Проверяем, есть ли INSERT_TEXT прямо перед уникальной строкой.
    # «Прямо перед» = на предыдущей непустой строке (пропускаем пустые).
    j = idx - 1
    while j >= 0 and lines[j].strip() == "":
        j -= 1

    if j >= 0 and INSERT_TEXT.strip() in lines[j]:
        return "skipped"

    # Вставляем: пустая строка + комментарий (с отступом якоря)
    indent = lines[idx][:len(lines[idx]) - len(lines[idx].lstrip())]
    lines.insert(idx, "\n")
    lines.insert(idx + 1, indent + INSERT_TEXT.strip() + "\n")

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return "inserted"

def main():
    counters = {"inserted": 0, "skipped": 0, "no-anchor": 0}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Пропускаем служебные папки
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
