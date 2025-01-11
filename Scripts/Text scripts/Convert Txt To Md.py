import os

def convert_txt_to_md():
    """
    Конвертирует все файлы с расширением .txt в папке, где находится скрипт,
    в файлы с расширением .md и удаляет оригинальные .txt файлы.
    """
    folder_path = os.path.dirname(os.path.abspath(__file__))
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                txt_file_path = os.path.join(root, file)
                md_file_path = os.path.splitext(txt_file_path)[0] + ".md"

                # Чтение содержимого .txt файла
                with open(txt_file_path, "r", encoding="utf-8") as txt_file:
                    content = txt_file.read()

                # Запись содержимого в .md файл
                with open(md_file_path, "w", encoding="utf-8") as md_file:
                    md_file.write(content)

                # Удаление оригинального .txt файла
                os.remove(txt_file_path)
                print(f"Конвертирован и удалён: {txt_file_path}")

if __name__ == "__main__":
    convert_txt_to_md()
    print("Готово! Все .txt файлы в папке скрипта конвертированы в .md и удалены.")
