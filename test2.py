import requests
from bs4 import BeautifulSoup
import csv
import time


def get_animals_count():
    """Получает количество животных по буквам алфавита с Википедии."""
    print("\nИнициализация словаря для подсчета животных...")
    russian_alphabet = [chr(i) for i in range(1040, 1072)]  # А-Я
    russian_alphabet.insert(6, 'Ё')  # Вставляем Ё после Е
    letter_counts = {letter: 0 for letter in russian_alphabet}
    print(f"Создан словарь для букв: {', '.join(russian_alphabet)}")

    base_url = "https://ru.wikipedia.org"
    current_url = base_url + "/wiki/Категория:Животные_по_алфавиту"
    page_num = 1

    print("\nНачинаем обработку страниц Википедии...")

    while current_url:
        try:
            print(f"\nОбработка страницы #{page_num} ({current_url})")

            # Загрузка страницы
            print("Загружаем страницу...", end=' ')
            start_time = time.time()
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
            load_time = time.time() - start_time
            print(f"успешно! (время загрузки: {load_time:.2f} сек)")

            # Парсинг страницы
            print("Парсим содержимое...", end=' ')
            soup = BeautifulSoup(response.text, 'html.parser')
            print("готово!")

            # Поиск блоков с категориями
            print("Ищем блоки с животными...", end=' ')
            category_groups = soup.find('div', class_='mw-category-columns') or \
                              soup.find('div', class_='mw-category')

            if not category_groups:
                print("\n⚠️ Не удалось найти блок с категориями")
                break
            print(f"найдено {len(category_groups.find_all('a'))} элементов")

            # Обработка всех ссылок
            print("Обрабатываем ссылки...")
            for link in category_groups.find_all('a'):
                title = link.get_text(strip=True)
                if title:
                    first_char = title[0].upper()
                    if first_char in letter_counts:
                        letter_counts[first_char] += 1

            # Поиск следующей страницы
            print("Проверяем наличие следующей страницы...", end=' ')
            next_page = soup.find('a', string='Следующая страница')
            if next_page:
                current_url = base_url + next_page['href']
                page_num += 1
                print(f"есть! ({current_url})")
            else:
                current_url = None
                print("это последняя страница")

            # Пауза между запросами
            time.sleep(1)

        except Exception as e:
            print(f"\n⚠️ Ошибка при обработке страницы: {e}")
            break

    return letter_counts


def save_to_csv(counts, filename='beasts.csv'):
    """Сохраняет результаты в CSV-файл."""
    print(f"\nСохранение результатов в файл {filename}...")
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Буква', 'Количество'])

        total = 0
        for letter in sorted(counts.keys()):
            writer.writerow([letter, counts[letter]])
            total += counts[letter]
            print(f"{letter}: {counts[letter]} записей")

    print(f"\nВсего обработано: {total} записей")
    print(f"Результаты сохранены в файл {filename}")


if __name__ == '__main__':
    print("=== Парсер животных с Википедии ===")
    start_time = time.time()

    try:
        counts = get_animals_count()
        save_to_csv(counts)

        total_time = time.time() - start_time
        print(f"\nПрограмма завершена за {total_time:.2f} секунд")

    except Exception as e:
        print(f"\n⚠️ Критическая ошибка: {e}")