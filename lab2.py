import csv
import random
import xml.dom.minidom
import os


def extract_year(year_str):
    if not year_str:
        return 0
    #отрезаем время '15.10.2021 9:22' -> '15.10.2021'
    date_part = year_str.strip().split()[0]
    digits = ''.join(ch for ch in date_part if ch.isdigit())
    if len(digits) >= 4:
        try:
            return int(digits[-4:])
        except ValueError:
            return 0
    return 0


def clean_str(text):
    # убираем лишние пробелы
    return text.replace('\xa0', ' ').strip()


def process_csv(filename='books.csv'):
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден.")
        return

    is_en = 'en' in filename.lower()


    COL_TITLE = 1
    if is_en:
        COL_AUTHOR = 2       
        COL_AUTHOR_ALT = 2   
        COL_YEAR = 3         # год
        COL_TARGET = 4       # издательство
        COL_POP = 5          # популярность
        min_year = 2000      
    else:
        COL_AUTHOR = 3       
        COL_AUTHOR_ALT = 4   
        COL_YEAR = 6         # дата
        COL_TARGET = 12      # жанр
        COL_POP = 8          # популярность
        min_year = 2018      

    # кодировка (windows-1251 или utf-8)
    encoding_to_use = 'utf-8'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            f.read(2048)
    except UnicodeDecodeError:
        encoding_to_use = 'cp1251'

    long_titles_count = 0
    all_records = []
    unique_items = set()
    book_popularity = []

    search_author = clean_str(
        input(f"\n[{filename}] Введите имя или фамилию автора (от {min_year} г.): ")
    )
    found_books = []
    older_books_count = 0

    with open(filename, 'r', encoding=encoding_to_use, newline='') as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader, None)  # скип шапку таблицы

        for row in reader:
            if len(row) <= max(COL_TITLE, COL_AUTHOR, COL_AUTHOR_ALT, COL_YEAR, COL_TARGET, COL_POP):
                continue

            title = clean_str(row[COL_TITLE])
            author_main = clean_str(row[COL_AUTHOR])
            author_alt = clean_str(row[COL_AUTHOR_ALT])
            # если поле 'Автор' пустое,то 'Автор (ФИО)'
            display_author = author_main if author_main else author_alt
            year = extract_year(row[COL_YEAR])

            # 1 названия длиннее 30 
            if len(title) > 30:
                long_titles_count += 1

            # 2. поиск
            if search_author:
                query = search_author.lower()
                if query in author_main.lower() or query in author_alt.lower():
                    if year >= min_year:
                        found_books.append(f"{display_author}. {title} - {year}")
                    else:
                        older_books_count += 1

            # генератор библиографических ссылок
            all_records.append(f"{display_author}. {title} - {year if year else 'б/г'}")

            # допзадание 1
            target_val = clean_str(row[COL_TARGET])
            if target_val:
                if is_en:
                    unique_items.add(target_val)
                else:
                    for tag in target_val.split('#'):
                        clean_tag = tag.strip()
                        if clean_tag:
                            unique_items.add(clean_tag)

            # допзадание 2
            try:
                pop = int(clean_str(row[COL_POP]))
            except ValueError:
                pop = 0
            book_popularity.append((f"{display_author} — «{title}»", pop))


    print(f"\n1. Количество записей с названием длиннее 30 символов: {long_titles_count}")


    print(f"\n2. Результаты поиска по автору «{search_author}» (от {min_year} года):")
    if found_books:
        print(f"   Найдено подходящих книг: {len(found_books)}")
        for b in found_books[:20]:
            print(f"   - {b}")
        if len(found_books) > 20:
            print(f"   ... и еще {len(found_books) - 20} книг.")
    else:
        print(f"   Книги от {min_year} года не найдены.")
        if older_books_count > 0:
            print(f"   (В базе есть {older_books_count} книг этого автора, но они старше {min_year} года)")


    sample_size = min(20, len(all_records))
    random_refs = random.sample(all_records, sample_size)
    output_txt = 'result.txt'
    with open(output_txt, 'w', encoding='utf-8') as out_f:
        for idx, ref in enumerate(random_refs, 1):
            out_f.write(f"{idx}. {ref}\n")

    print(f"\n3. 20 библиографических ссылок (сохранены в {output_txt}):")
    for idx, ref in enumerate(random_refs, 1):
        print(f"   {idx}. {ref}")


    label = "издательств" if is_en else "тегов (жанров)"
    print(f"\nДопзадание 1. Перечень всех {label} без повторений ({len(unique_items)} шт.):")
    print("   " + ", ".join(sorted(unique_items)))


    book_popularity.sort(key=lambda x: x[1], reverse=True)
    print("\nДопзадание 2. Самые популярные 20 книг:")
    for idx, (book_info, pop) in enumerate(book_popularity[:20], 1):
        print(f"   {idx}. {book_info} (выдач/скачиваний: {pop})")


def process_xml(filename='currency.xml'):
    if not os.path.exists(filename):
        print(f"\nФайл {filename} не найден.")
        return

    dom = xml.dom.minidom.parse(filename)
    dom.normalize()

    currency_dict = {}
    for valute in dom.getElementsByTagName('Valute'):
        name_nodes = valute.getElementsByTagName('Name')
        char_nodes = valute.getElementsByTagName('CharCode')
        if name_nodes and char_nodes:
            name = name_nodes[0].firstChild.data.strip()
            char_code = char_nodes[0].firstChild.data.strip()
            currency_dict[name] = char_code

    print("\n4. Словарь валют «Name - CharCode» из currency.xml:")
    for name, code in currency_dict.items():
        print(f"   {name}: {code}")


if __name__ == '__main__':
    process_csv('books.csv')
    process_csv('books-en.csv')
    process_xml('currency.xml')