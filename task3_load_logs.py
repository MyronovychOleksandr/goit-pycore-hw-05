import sys
from collections import Counter
from pathlib import Path


def count_logs_by_level(logs: list) -> dict:
    return Counter([log["level"] for log in logs])


def parse_log_line(line: str) -> dict:
    line_args = line.split(maxsplit=3)
    date, time, level, message = line_args
    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str) -> list:
    lines = []
    logs = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"File with path {file_path} not found!")
    except UnicodeDecodeError:
        print(f"File {file_path} is not a valid text file!")


    for i, line in enumerate(lines, start=1):
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
        try:
            parsed_log = parse_log_line(cleaned_line)
            logs.append(parsed_log)
        except (IndexError, ValueError):
            print(f"Пропущено рядок {i}: {cleaned_line}")

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda x: x["level"].lower() == level.lower(), logs))


def display_log_counts(counts: dict) -> None:
    print(f"{'Рівень логування':<17}| Кількість")
    print(f"{'-' * 17}|{'-' * 10}")
    for level, count in counts.items():
        print(f"{level:<17}| {count}")


def main():
    if len(sys.argv) == 1:
        print("Команда без параметрів!")
        sys.exit(1)

    file = Path(sys.argv[1]).resolve()
    if not file.is_file():
        print(f"Помилка: '{file}' не існує або це не файл")
        sys.exit(1)

    level_arg = ""
    if len(sys.argv) >= 3:
        level_arg = sys.argv[2]

    logs = load_logs(file) 
    
    counts = count_logs_by_level(logs)
    
    display_log_counts(counts)

    if not level_arg:
        return
    
    logs_by_level = filter_logs_by_level(logs, level_arg)

    if not logs_by_level:
        print("Записів не знайдено")
        return
    
    print(f"Деталі логів для рівня '{level_arg.upper()}':")
    for log in logs_by_level:
        print(f"{log['date']} {log['time']} - {log['message']}")




if __name__ == "__main__":
    main()