import os
import re

def clean_markdown(file_name, remove_links=False, remove_hashtags=False, words_to_remove=None):
    """
    Очищает файл по заданным параметрам.
    :param file_name: Имя файла для обработки.
    :param remove_links: Удалить ли все ссылки.
    :param remove_hashtags: Удалить ли слова-хэштеги (начинаются с #).
    :param words_to_remove: Список слов и предложений для удаления.
    """
    # Читаем содержимое файла
    with open(file_name, "r", encoding="utf-8") as file:
        content = file.read()

    # Удаляем ссылки, если выбрано
    if remove_links:
        content = re.sub(r"\[.*?\]\(.*?\)", "", content)  # Markdown-ссылки
        content = re.sub(r"https?://\S+", "", content)  # Обычные URL
        print(f"Ссылки удалены в файле: {file_name}")

    # Удаляем хэштеги, если выбрано
    if remove_hashtags:
        content = re.sub(r"\s?#\S+", "", content)  # Удаляем хэштеги
        print(f"Хэштеги удалены в файле: {file_name}")

    # Удаляем указанные слова и предложения
    if words_to_remove:
        for word in words_to_remove:
            if word.startswith("(") and word.endswith(")"):  # Если это предложение в скобках
                word_content = word[1:-1].strip()  # Убираем скобки и пробелы
                # Удаляем текст с учётом пробелов вокруг
                content = re.sub(rf"(\s|^){re.escape(word_content)}(\s|$)", " ", content)
            else:  # Удаляем одиночное слово
                content = re.sub(rf"\b{re.escape(word)}\b", "", content)
        print(f"Удалены слова и предложения в файле {file_name}: {', '.join(words_to_remove)}.")

    # Формируем имя для нового файла
    base_name, _ = os.path.splitext(file_name)
    output_file = f"{base_name}_cleaned.txt"

    # Сохраняем результат в новый файл
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"Файл успешно обработан и сохранён как: {output_file}")

if __name__ == "__main__":
    # Параметры для удаления
    remove_links = input("Удалить все ссылки? (да/нет): ").strip().lower() == "да"
    remove_hashtags = input("Удалить все хэштеги (#)? (да/нет): ").strip().lower() == "да"
    words_input = input("Введите слова для удаления через пробел. Если это предложение, оберните его в скобки: ").strip()
    words_to_remove = words_input.split(" ") if words_input else None

    # Поиск всех файлов с расширением .md и .txt в текущей папке
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files_to_process = [f for f in os.listdir(current_dir) if f.endswith((".md", ".txt"))]

    if not files_to_process:
        print("Нет файлов с расширениями .md или .txt для обработки.")
    else:
        for file in files_to_process:
            clean_markdown(file, remove_links, remove_hashtags, words_to_remove)
