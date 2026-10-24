import csv
import random
import xml.dom.minidom
import os

def process_csv(filename='books.csv'):
    print(f"--- Обработка файла {filename} ---")


    # определяем англ файл или русс
    is_en = 'en' in filename.lower()

    # индексы колонок
    COL_TITLE = 1
    COL_AUTHOR = 2
    COL_YEAR = 3
    
    if is_en:
        COL_TARGET = 4  # publisher 
        COL_POP = 5     # downloads 
        min_year = 2000
    else:
        COL_TARGET = 12 # канр книги / теги 
        COL_POP = 8     # кол-во выдач 
        min_year = 2018 

    long_title_count = 0
    search_author = input("Введите имя автора для поиска: ").strip().lower()
    found_books = []
    all_books = []
    
    # структуры для допзадания
    unique_items = set()
    book_popularity = []

    try:
        with open(filename, 'r', encoding='windows-1251') as f:
            reader = csv.reader(f, delimiter=';')
            headers = next(reader, None) # пропуск заголовка

            for row in reader:
                # пропускаем битые строки
                if len(row) <= max(COL_TITLE, COL_AUTHOR, COL_YEAR, COL_TARGET, COL_POP):
                    continue
                
                title = row[COL_TITLE]
                author = row[COL_AUTHOR]
                year_str = row[COL_YEAR]
                target_val = row[COL_TARGET].strip()

                # --- основное задание---
                if len(title) > 30:
                    long_title_count += 1

                try:
                    year = int(year_str[-4:])
                except ValueError:
                    year = 0

                if search_author and search_author in author.lower() and year >= min_year:
                    found_books.append(row)

                all_books.append((author, title, year_str))

                # --- допзадание ---
                # 1 Уникальные теги / издательства
                if is_en:
                    if target_val:
                        unique_items.add(target_val)
                else:
                    # делим теги по символу #
                    tags = [t.strip() for t in target_val.split('#') if t.strip()]
                    for t in tags:
                        unique_items.add(t)
                        
                # 2 подсчет популярности (Downloads)
                try:
                    pop_val = int(row[COL_POP])
                except ValueError:
                    pop_val = 0
                book_popularity.append((title, pop_val))


        print(f"\n[ОСНОВНОЕ] 1. Записей с названием длиннее 30 символов: {long_title_count}")
        print(f"[ОСНОВНОЕ] 2. Поиск по автору (год >= {min_year}): Найдено {len(found_books)}")
        for b in found_books[:5]:
            print(f"   - {b[COL_AUTHOR]}. {b[COL_TITLE]} ({b[COL_YEAR]})")
            
        if len(all_books) >= 20:
            sample_books = random.sample(all_books, 20)
        else:
            sample_books = all_books

        print("\n[ОСНОВНОЕ] 3. 20 случайных библиографических ссылок (сохранены в файл):")
        with open(f"links_{filename.split('.')[0]}.txt", "w", encoding="utf-8") as txt_file:
            for i, (author, title, year) in enumerate(sample_books, 1):
                line = f"{i}. {author}. {title} - {year}"
                print(f"   {line}") # Вывод в консоль для наглядности (опционально)
                txt_file.write(line + "\n")

        # доп задание
        print("\n--- ДОПОЛНИТЕЛЬНЫЕ ЗАДАНИЯ ---")
        if is_en:
            print(f"1. Перечень издательств без повторений (Всего: {len(unique_items)}):")
        else:
            print(f"1. Перечень всех тегов без повторений (Всего: {len(unique_items)}):")
        
        # первые 10 для примера
        print("   Примеры:", list(unique_items)[:10])

        # сортируем по убыванию популярности
        book_popularity.sort(key=lambda x: x[1], reverse=True)
        print("\n2. Самые популярные 20 книг:")
        for i, (title, pop) in enumerate(book_popularity[:20], 1):
            print(f"   {i}. {title} (Популярность: {pop})")

    except UnicodeDecodeError:
        print("Ошибка кодировки. Попробуйте поменять 'windows-1251' на 'utf-8'.")


def process_xml(filename='currency.xml'):
    print(f"\n--- Обработка файла {filename} ---")
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден.")
        return

    currency_dict = {}
    try:
        dom = xml.dom.minidom.parse(filename)
        dom.normalize()
        valutes = dom.getElementsByTagName("Valute")

        for node in valutes:
            name_node = node.getElementsByTagName("Name")[0]
            charcode_node = node.getElementsByTagName("CharCode")[0]
            
            name = name_node.firstChild.nodeValue
            charcode = charcode_node.firstChild.nodeValue
            
            currency_dict[name] = charcode

        print("[ОСНОВНОЕ XML] 4. Словарь Name-CharCode успешно создан. Пример данных:")
        for i, (name, code) in enumerate(currency_dict.items()):
            if i >= 5: break
            print(f"  {name}: {code}")

    except Exception as e:
        print(f"Ошибка при разборе XML: {e}")


if __name__ == '__main__':
    # скрипт автоматически определит структуру в зависимости от названия файла
    process_csv('books.csv')
    process_csv('books-en.csv') # если нужно проверить англ. файл
    process_xml('currency.xml')
