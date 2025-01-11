import os
import json
from bs4 import BeautifulSoup

# Загружаем настройки из config.json
try:
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("Ошибка: файл config.json не найден. Поместите config.json в ту же папку, что и скрипт.")
    exit(1)
except json.JSONDecodeError:
    print("Ошибка: файл config.json содержит недопустимый JSON. Проверьте его синтаксис.")
    exit(1)

MIN_WORDS = config.get("min_words", 5)
OUTPUT_FILE = config.get("output_file", "result.txt")  # Изменено расширение на .txt
LOG_FILE = config.get("log_file", "process_log.txt")
HTML_FILES_PATTERN = config.get("html_files_pattern", "messages")
SEPARATOR = config.get("separator", "---")

def log(message):
    """Функция для записи логов в файл."""
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")
    print(message)  # Одновременно выводим сообщение в терминал

def extract_text_from_html(file_path, seen_messages):
    """Извлекает текст из HTML-файла и возвращает отфильтрованные сообщения."""
    log(f"Обработка файла: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as html_file:
            soup = BeautifulSoup(html_file, "lxml")
    except Exception as e:
        log(f"Ошибка при чтении файла {file_path}: {e}")
        return []

    messages = []
    for message_div in soup.find_all("div", class_="message"):
        text_div = message_div.find("div", class_="text")
        if not text_div:
            continue  # Пропустить сообщения без текста

        text = text_div.get_text(strip=True)
        word_count = len(text.split())
        if word_count >= MIN_WORDS and text not in seen_messages:
            seen_messages.add(text)
            messages.append(text)

    log(f"Найдено сообщений: {len(messages)}")
    return messages

def main():
    """Основная функция."""
    seen_messages = set()  # Для хранения уникальных сообщений
    all_messages = []

    # Поиск всех HTML-файлов в директории
    html_files = [f for f in os.listdir() if f.startswith(HTML_FILES_PATTERN) and f.endswith(".html")]
    if not html_files:
        log("Ошибка: не найдено HTML-файлов для обработки.")
        exit(1)

    log(f"Найдено файлов для обработки: {len(html_files)}")

    for file in html_files:
        messages = extract_text_from_html(file, seen_messages)
        all_messages.extend(messages)

    if not all_messages:
        log("Предупреждение: не найдено подходящих сообщений для сохранения.")
    else:
        # Сохранение всех сообщений в TXT-файл
        try:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as txt_file:
                for i, message in enumerate(all_messages):
                    txt_file.write(f"{message}\n")
                    if i < len(all_messages) - 1:  # Добавляем разделитель только между сообщениями
                        txt_file.write(f"{SEPARATOR}\n")
            log(f"Обработка завершена. Итоговый файл: {OUTPUT_FILE}")
        except Exception as e:
            log(f"Ошибка при записи в файл {OUTPUT_FILE}: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"Неожиданная ошибка: {e}")
