
import argparse
import csv
import sys
from tabulate import tabulate

AGGREGATIONS = {    # это список агрегаторов (последний добавил для проверки)
    'avg': lambda values: sum(values) / len(values) if values else None,
    'min': min,
    'max': max,
    'avg*2': lambda values: 2*sum(values) / len(values) if values else None,
    # тут можно добавить свой агрегатор в формате "агрегатор": функция
}

def parse_args() -> argparse.Namespace:    # тут парсим аргументы с введённой команды   
    parser = argparse.ArgumentParser(description='Обработка CSV: фильтрация и агрегация')
    parser.add_argument('--file', required=True, help='Путь к CSV-файлу')
    parser.add_argument('--where', help='Условие фильтрации, например: "price>1000" или "brand=apple"')
    parser.add_argument('--aggregate', help='Агрегация, например: "avg:price", "min:rating", "max:price"')
    args = parser.parse_args()
    if args.where and args.aggregate:
        parser.error('Нельзя использовать --where и --aggregate одновременно.')
    return args


def read_csv(file_path: str) -> list[dict]:     # тут читаем данные из файла
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            if not data:
                print('Файл пустой или не содержит данных.')
                sys.exit(1)
            return data
    except FileNotFoundError:
        print(f'Файл не найден: {file_path}')
        sys.exit(1)
    except Exception as e:
        print(f'Ошибка при чтении файла: {e}')
        sys.exit(1)


def filter_rows(rows: list[dict], where: str | None) -> list[dict]:    # тут определяем фильтр и фильтруем
    if not where:
        return rows
    for op in ('>=', '<=', '>', '<', '='):
        idx = where.find(op)
        if idx != -1:
            key = where[:idx].strip()
            value = where[idx+len(op):].strip()
            operator = op
            break
    else:
        print('Некорректный формат фильтра. Используйте column<value, column>value или column=value')
        sys.exit(1)
    if key not in rows[0]:
        print(f'Колонка "{key}" не найдена в файле.')
        sys.exit(1)
    def cmp(row):
        v = row.get(key, '')
        try:
            v = float(v)
            value_num = float(value)
        except ValueError:
            v = str(v)
            value_num = value
        if operator == '=':
            return v == value_num
        elif operator == '>':
            return v > value_num
        elif operator == '<':
            return v < value_num
        elif operator == '>=':
            return v >= value_num
        elif operator == '<=':
            return v <= value_num
        else:
            return False
    filtered = [row for row in rows if cmp(row)]
    if not filtered:
        print('Нет данных, удовлетворяющих условию фильтрации.')
        sys.exit(0)
    return filtered


def aggregate_rows(rows: list[dict], aggregate: str | None):    # здесь применяем функцию агрегации
    if not aggregate:
        return None
    if ':' not in aggregate:
        print(f'Некорректный формат агрегации. Используйте avg:column, min:column и т.д.')
        sys.exit(1)
    func, col = aggregate.split(':', 1)
    func = func.strip()
    col = col.strip()
    if func not in AGGREGATIONS:
        print(f'Неизвестная агрегация: {func}')
        sys.exit(1)
    if col not in rows[0]:
        print(f'Колонка "{col}" не найдена в файле.')
        sys.exit(1)
    try:
        values = [float(row[col]) for row in rows]
    except Exception:
        print(f'Колонка {col} должна быть числовой для агрегации')
        sys.exit(1)
    if not values:
        print('Нет данных для агрегации.')
        sys.exit(0)
    result = AGGREGATIONS[func](values)
    return {'aggregation': func, 'column': col, 'value': result}


def print_table(rows: list[dict]) -> None:  # тут выводим таблицы
    if not rows:
        print('Нет данных для вывода.')
        return
    print(tabulate(rows, headers="keys", tablefmt='grid'))


def print_aggregate(result) -> None:    # тут выводим данные после агрегации
    if not result:
        print('Нет данных для агрегации.')
        return
    print(tabulate([[result['aggregation'], result['column'], result['value']]], headers=["agg", "column", "value"], tablefmt='grid'))


def main() -> None:
    args = parse_args()
    rows = read_csv(args.file)
    if args.aggregate:
        result = aggregate_rows(rows, args.aggregate)
        print_aggregate(result)
    else:
        rows = filter_rows(rows, args.where)
        print_table(rows)

if __name__ == '__main__':
    main() 