Инструкция к запуску:

1. Создайте виртуальное окружение:

   python3 -m venv .venv

   source .venv/bin/activate

3. Установите зависимости:

   pip install -r requirements.txt

5. Запустите скрипт с нужными параметрами:

   python3 main.py --file <путь_к_csv> [--where "колонка=значение"] [--aggregate "агрегатор:колонка"]

Примеры:
   
   python3 main.py --file products.csv --where "brand=apple"
   
   python3 main.py --file products.csv --aggregate "avg:price"

Инструкция к запуску через Docker:

1. Соберите образ:

   docker build -t csv-viewer .

3. Запустите контейнер с вашим файлом:

   docker run python3 main.py --file <путь_к_csv> [--where "колонка=значение"] [--aggregate "агрегатор:колонка"]

Инструкция к запуску тестов:

1. Убедитесь, что установлены зависимости (см. выше).
2. Запустите тесты командой:

   pytest test_main.py

Инструкция к добавлению агрегаторов:

1. Откройте main.py
2. Найдите словарь AGGREGATIONS в начале файла.
3. Добавьте новую строку вида:
   'имя_агрегатора': функция,
   Например, чтобы добавить медиану:

   import statistics
   AGGREGATIONS['median'] = statistics.median

4. Теперь можно использовать новый агрегатор в параметре --aggregate, например:

   python3 main.py --file products.csv --aggregate "median:price"
