import os
import re

def remove_bracketed_text(text):
    """
    Удаляет текст, заключённый в квадратные скобки, например, [музыка].
    """
    return re.sub(r'\[.*?\]', '', text)

def srt_to_txt(srt_file_path, txt_file_path):
    """
    Конвертирует .srt файл в .txt, удаляя временные метки, номера строк и текст в квадратных скобках.
    
    :param srt_file_path: Путь к исходному .srt файлу
    :param txt_file_path: Путь к результирующему .txt файлу
    """
    try:
        with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
            lines = srt_file.readlines()
    except UnicodeDecodeError:
        # Если не удалось открыть с кодировкой utf-8, пробуем iso-8859-1
        with open(srt_file_path, 'r', encoding='iso-8859-1') as srt_file:
            lines = srt_file.readlines()

    txt_lines = []
    subtitle_block = []
    
    for line in lines:
        line = line.strip()
        
        if line.isdigit():
            # Пропускаем номера субтитров
            continue
        elif re.match(r'\d{2}:\d{2}:\d{2}[.,]\d{3} -->', line):
            # Пропускаем временные метки
            continue
        elif line == '':
            # Конец блока субтитров
            if subtitle_block:
                # Объединяем строки внутри блока
                subtitle_text = ' '.join(subtitle_block)
                # Удаляем текст в квадратных скобках
                subtitle_text = remove_bracketed_text(subtitle_text)
                # Удаляем лишние пробелы
                subtitle_text = re.sub(r'\s+', ' ', subtitle_text).strip()
                if subtitle_text:
                    txt_lines.append(subtitle_text)
                # Сбрасываем блок
                subtitle_block = []
        else:
            # Добавляем строку в текущий блок субтитров
            subtitle_block.append(line)
    
    # Обработка последнего блока, если файл не заканчивается пустой строкой
    if subtitle_block:
        subtitle_text = ' '.join(subtitle_block)
        subtitle_text = remove_bracketed_text(subtitle_text)
        subtitle_text = re.sub(r'\s+', ' ', subtitle_text).strip()
        if subtitle_text:
            txt_lines.append(subtitle_text)
    
    # Создаём директорию TXT внутри output_dir, если она не существует
    txt_dir = os.path.join(os.path.dirname(txt_file_path), 'TXT')
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
    
    # Определяем путь для сохранения .txt файла
    final_txt_path = os.path.join(txt_dir, os.path.basename(txt_file_path))
    
    # Записываем текст в .txt файл
    with open(final_txt_path, 'w', encoding='utf-8') as txt_file:
        for line in txt_lines:
            txt_file.write(line + '\n')
    
    print(f"Сохранено: {final_txt_path}")

def convert_all_srt_to_txt(subtitles_dir='subtitles'):
    """
    Находит все .srt файлы в указанной директории и конвертирует их в .txt.
    
    :param subtitles_dir: Директория с .srt файлами
    """
    if not os.path.exists(subtitles_dir):
        print(f"Директория '{subtitles_dir}' не найдена.")
        return

    # Создаём папку TXT внутри subtitles_dir, если она не существует
    txt_dir = os.path.join(subtitles_dir, 'TXT')
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
    
    for filename in os.listdir(subtitles_dir):
        if filename.lower().endswith('.srt'):
            srt_path = os.path.join(subtitles_dir, filename)
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(subtitles_dir, txt_filename)
            srt_to_txt(srt_path, txt_path)

def main():
    """
    Основная функция скрипта.
    """
    subtitles_dir = 'subtitles'  # Папка с .srt файлами
    convert_all_srt_to_txt(subtitles_dir)
    print("\nВсе файлы .srt были успешно конвертированы в .txt и сохранены в папке 'subtitles\\TXT'.")

if __name__ == "__main__":
    main()
