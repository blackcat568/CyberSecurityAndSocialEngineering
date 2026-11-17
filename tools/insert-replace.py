#!/usr/bin/env python3
"""
Заменяет ТОЧНО заданный многострочный блок на короткий вариант.

- Ищет блок по точному совпадению (с учётом переносов строк).
- Пробелы/табы в начале строк ИГНОРИРУЮТСЯ при сравнении
  (блок может быть с отступом или без).
- Если блок не найден — файл НЕ трогается, выводится в отчёт
  «требует ручной проверки».
- Идемпотентен: если короткий вариант уже стоит — пропускается.

Использование (из корня репозитория):
    python3 tools/insert-replace.py
"""

import os
import re
import sys

# ==================== CONFIG ====================
# Старый блок, который нужно заменить (задаём ЖЁСТКО, как есть).
# Отступы в начале строк можно не соблюдать — они игнорируются.
OLD_BLOCK = '''<button id="panel-toggle" style="
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 10000;
  padding: 8px 14px;
  cursor: pointer;
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  font-size: 0.9rem;
">
  📚 Articles
</button>'''

NEW_BLOCK = '''<button id="panel-toggle">📚 Articles</button>'''

MARKER = '<button id="panel-toggle">📚 Articles</button>'
# ================================================

ROOT = "."
SKIP_DIRS = {".git", "node_modules", "assets", "pictures", ".github"}


def normalize_block(block: str) -> str:
    """
    Нормализует блок для сравнения:
    - убирает ведущие пробелы/табы в каждой строке,
    - убирает пустые строки в начале/конце,
    - нормализует переносы строк (CRLF → LF).
    """
    lines = block.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    stripped = [ln.lstrip(" \t") for ln in lines]
    # убрать пустые строки в начале и конце
    while stripped and stripped[0] == "":
        stripped.pop(0)
    while stripped and stripped[-1] == "":
        stripped.pop()
    return "\n".join(stripped)


def process_file(path: str) -> str:
    """
    Возвращает статус:
      'replaced'  — блок найден и заменён
      'skipped'   — короткий вариант уже стоит
      'no-block'  — блок НЕ найден, требует ручной проверки
      'error'     — ошибка чтения/записи
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # Идемпотентность
    if MARKER in text:
        return "skipped"

    # Нормализуем текст файла и старый блок для поиска
    text_norm = text.replace("\r\n", "\n").replace("\r", "\n")
    old_norm = normalize_block(OLD_BLOCK)

    # Ищем блок построчно, игнорируя ведущие пробелы.
    # Собираем «окно» строк файла такой же длины, как блок,
    # и сравниваем нормализованные строки.
    file_lines = text_norm.split("\n")
    block_lines = old_norm.split("\n")
    n = len(block_lines)

    if n == 0:
        return "error"

    match_start = None
    for i in range(len(file_lines) - n + 1):
        window = [ln.lstrip(" \t") for ln in file_lines[i:i + n]]
        # убрать пустые в начале/конце окна (на случай, если в файле
        # вокруг блока есть пустые строки, а в OLD_BLOCK их нет)
        while window and window[0] == "":
            window.pop(0)
        while window and window[-1] == "":
            window.pop()
        if window == block_lines:
            match_start = i
            break

    if match_start is None:
        return "no-block"

    # Определяем реальные границы блока в исходном тексте:
    # от начала строки match_start до конца строки match_start + n - 1.
    # Чтобы сохранить отступ/переносы, работаем с исходным text_norm.
    # Вычисляем позиции начала и конца в символах.
    lines_with_end = text_norm.split("\n")
    start_char = sum(len(ln) + 1 for ln in lines_with_end[:match_start])
    # конец блока — конец строки match_start + n - 1 (включая её длину)
    end_char = start_char + sum(len(ln) + 1 for ln in lines_with_end[match_start:match_start + n])
    # убираем лишний \n в конце (он относится к следующей строке)
    end_char -= 1

    # Заменяем
    new_text = text_norm[:start_char] + NEW_BLOCK + text_norm[end_char:]

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    return "replaced"


def main():
    counters = {"replaced": 0, "skipped": 0, "no-block": 0, "error": 0}
    manual = []  # файлы, требующие ручной проверки

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for name in filenames:
            if not name.lower().endswith((".html", ".htm")):
                continue
            path = os.path.join(dirpath, name)
            try:
                status = process_file(path)
            except Exception as e:
                print(f"[ERROR]     {path}: {e}")
                counters["error"] += 1
                continue

            counters[status] += 1
            print(f"[{status.upper():9}] {path}")
            if status == "no-block":
                manual.append(path)

    print("\nИтого:")
    print(f"  заменено:         {counters['replaced']}")
    print(f"  пропущено (уже):  {counters['skipped']}")
    print(f"  без блока:        {counters['no-block']}")
    print(f"  ошибок:           {counters['error']}")

    if manual:
        print("\n=== ТРЕБУЮТ РУЧНОЙ ПРОВЕРКИ (блок не найден) ===")
        for p in manual:
            print(f"  - {p}")


if __name__ == "__main__":
    sys.exit(main())
