import argparse
import re
import sys
from typing import List


def fractional_day_to_utc(date_str: str, sec_precision: int = 3) -> str:
    """Конвертує рядок вигляду '2026 09 05.97824103' у формат 'YYYY-MM-DD HH:MM:SS.sss UTC'."""
    pattern = r"(\d{4})[\s\-\.]+(\d{1,2})[\s\-\.]+(\d{1,2})\.(\d+)"
    match = re.search(pattern, date_str.strip())

    if not match:
        raise ValueError(f"Некоректний формат дати: '{date_str}'")

    year, month, day_int, frac_str = match.groups()
    frac_day = float("0." + frac_str)

    total_hours = frac_day * 24.0
    hours = int(total_hours)

    total_minutes = (total_hours - hours) * 60.0
    minutes = int(total_minutes)

    seconds = (total_minutes - minutes) * 60.0

    fmt_sec = f"{seconds:.{sec_precision}f}"
    if float(fmt_sec) >= 60.0:
        seconds = 0.0
        minutes += 1
        if minutes >= 60:
            minutes = 0
            hours += 1

    return f"{year}-{int(month):02d}-{int(day_int):02d} {hours:02d}:{minutes:02d}:{seconds:0{sec_precision+3}.{sec_precision}f} UTC"


def process_dates(dates: List[str], precision: int) -> None:
    for d in dates:
        try:
            res = fractional_day_to_utc(d, precision)
            print(f"{d} -> {res}")
        except ValueError as e:
            print(f"Помилка: {e}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="astro2utc",
        description="CLI-утиліта для конвертації дробових астрономічних днів у стандартний формат UTC.",
    )
    parser.add_argument(
        "dates",
        nargs="*",
        help="Дати для конвертації (наприклад: '2026 09 05.97824103')",
    )
    parser.add_argument(
        "-p",
        "--precision",
        type=int,
        default=3,
        help="Точність секунд (знаків після коми, за замовчуванням: 3)",
    )

    args = parser.parse_args()

    if args.dates:
        process_dates(args.dates, args.precision)
        return

    if not sys.stdin.isatty():
        lines = [line.strip() for line in sys.stdin if line.strip()]
        process_dates(lines, args.precision)
        return

    print("Астрономічний конвертер часу (Ctrl+C для виходу)")
    try:
        while True:
            line = input("> ").strip()
            if line:
                process_dates([line], args.precision)
    except (KeyboardInterrupt, EOFError):
        print("\nЗавершено.")


if __name__ == "__main__":
    main()