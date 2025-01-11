import yt_dlp
import os
import re
import subprocess

def get_playlist_info(playlist_url):
    """
    Извлекает информацию о плейлисте, включая общее количество видео.
    
    :param playlist_url: URL плейлиста YouTube
    :return: Общее количество видео в плейлисте
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,  # Не извлекает подробности каждого видео
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
    
    if 'entries' not in info_dict:
        print("Не удалось извлечь информацию о плейлисте.")
        return 0
    
    total_videos = len(info_dict['entries'])
    print(f"Общее количество видео в плейлисте: {total_videos}")
    return total_videos

def download_subtitles(playlist_url, output_dir='subtitles', languages=['en']):
    """
    Скачивает субтитры с YouTube-плейлиста и сохраняет их с номерами.
    
    :param playlist_url: URL плейлиста YouTube
    :param output_dir: Директория для сохранения субтитров
    :param languages: Список языковых кодов для субтитров (например, ['en', 'ru'])
    :return: Список номеров видео, для которых не удалось скачать субтитры
    """
    # Создаём директорию для субтитров, если её нет
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Список для хранения номеров видео, у которых не удалось скачать субтитры
    failed_numbers = []
    
    ydl_opts = {
        'ignoreerrors': True,
        'skip_download': True,  # Не загружать видео
        'writesubtitles': True,
        'writeautomaticsub': True,  # Загрузить автоматические субтитры, если ручные недоступны
        'subtitleslangs': languages,  # Языки субтитров, например ['en', 'ru']
        'subtitlesformat': 'vtt',  # Скачивать в формате .vtt для последующей конвертации
        'outtmpl': os.path.join(output_dir, '%(playlist_index)03d.%(title)s.%(ext)s'),  # Нумерация с ведущими нулями
        'playlistend': 1000,  # Максимальное количество видео в плейлисте
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Получаем информацию о плейлисте для определения общего количества видео
        playlist_info = ydl.extract_info(playlist_url, download=False)
        if 'entries' not in playlist_info:
            print("Не удалось извлечь информацию о плейлисте.")
            return []
        total_videos = len(playlist_info['entries'])
        print(f"Общее количество видео в плейлисте: {total_videos}")
        
        # Скачиваем субтитры
        ydl.download([playlist_url])
    
    # Проверяем, какие номера не имеют соответствующих файлов
    for i in range(1, total_videos + 1):
        number_str = f"{i:03d}"
        # Ожидается, что файл субтитров будет иметь формат '001.НазваниеВидео.vtt'
        vtt_filename = f"{number_str}."
        found = False
        for file in os.listdir(output_dir):
            if file.startswith(vtt_filename) and file.lower().endswith('.vtt'):
                found = True
                break
        if not found:
            failed_numbers.append(number_str)
            print(f"Субтитры не найдены для видео номер: {number_str}")
    
    return failed_numbers

def convert_vtt_to_srt(vtt_file_path, srt_file_path):
    """
    Конвертирует .vtt файл в .srt с помощью ffmpeg.
    
    :param vtt_file_path: Путь к исходному .vtt файлу
    :param srt_file_path: Путь к результирующему .srt файлу
    """
    command = [
        'ffmpeg',
        '-i', vtt_file_path,
        srt_file_path
    ]
    try:
        # Запуск команды ffmpeg без вывода в консоль
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Конвертировано: {vtt_file_path} -> {srt_file_path}")
        # Удаляем оригинальный .vtt файл после успешной конвертации
        os.remove(vtt_file_path)
        print(f"Удалён оригинальный файл: {vtt_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка конвертации {vtt_file_path}: {e}")

def remove_duplicate_lines(srt_file_path):
    """
    Удаляет дублирующиеся строки и текст в квадратных скобках в .srt файле.
    
    :param srt_file_path: Путь к .srt файлу
    """
    try:
        with open(srt_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(srt_file_path, 'r', encoding='iso-8859-1') as file:
            lines = file.readlines()

    unique_subtitles = []
    previous_text = ""

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.isdigit() or re.match(r'\d{2}:\d{2}:\d{2}[.,]\d{3} -->', stripped_line) or stripped_line == '':
            # Пропускаем номера субтитров, временные метки и пустые строки
            unique_subtitles.append(line)
            continue

        # Удаляем текст в квадратных скобках
        cleaned_line = re.sub(r'\[.*?\]', '', stripped_line)

        if cleaned_line == previous_text:
            # Пропускаем дублирующуюся строку
            continue
        else:
            unique_subtitles.append(line)
            previous_text = cleaned_line

    # Записываем уникальные субтитры обратно в файл
    with open(srt_file_path, 'w', encoding='utf-8') as file:
        for line in unique_subtitles:
            file.write(line)

    print(f"Удалены дубликаты и лишние элементы в файле: {srt_file_path}")

def convert_all_vtt_to_srt_and_cleanup(subtitles_dir='subtitles'):
    """
    Находит все .vtt файлы в указанной директории и конвертирует их в .srt,
    затем удаляет дубликаты строк и текст в квадратных скобках в полученных .srt файлах.
    
    :param subtitles_dir: Директория с субтитрами
    """
    for filename in os.listdir(subtitles_dir):
        if filename.lower().endswith('.vtt'):
            vtt_path = os.path.join(subtitles_dir, filename)
            srt_filename = os.path.splitext(filename)[0] + '.srt'
            srt_path = os.path.join(subtitles_dir, srt_filename)
            convert_vtt_to_srt(vtt_path, srt_path)
            remove_duplicate_lines(srt_path)

def write_error_log(missing_numbers, error_file_path='errors.txt'):
    """
    Записывает список отсутствующих номеров в файл с ошибками.
    
    :param missing_numbers: Список номеров видео, для которых не удалось скачать субтитры
    :param error_file_path: Путь к файлу с ошибками
    """
    total_failures = len(missing_numbers)
    if total_failures == 0:
        print("Все субтитры были успешно скачаны.")
        return

    with open(error_file_path, 'w', encoding='utf-8') as error_file:
        error_file.write("Список номеров видео, для которых не удалось скачать субтитры:\n\n")
        for number in missing_numbers:
            error_file.write(f"{number}\n")
        error_file.write(f"\nОбщее количество неудачных попыток скачивания субтитров: {total_failures}\n")

    print(f"Файл с ошибками создан: {error_file_path}")
    print(f"Всего неудачных попыток: {total_failures}")

def main():
    """
    Основная функция скрипта.
    """
    playlist_link = input("Введите ссылку на плейлист YouTube: ").strip()
    desired_languages_input = input("Введите коды языков субтитров через запятую (например, en,ru): ").strip()
    desired_languages = [lang.strip() for lang in desired_languages_input.split(',') if lang.strip()]

    if not playlist_link:
        print("Ссылка на плейлист не может быть пустой.")
        return

    if not desired_languages:
        print("Необходимо указать хотя бы один язык субтитров.")
        return

    print("\nНачинаем определение общего количества видео в плейлисте...")
    total_videos = get_playlist_info(playlist_link)
    if total_videos == 0:
        print("Не удалось определить количество видео в плейлисте. Завершаем работу скрипта.")
        return

    print("\nНачинаем загрузку субтитров...")
    failed_numbers = download_subtitles(playlist_link, languages=desired_languages)
    print("Загрузка субтитров завершена.\n")

    print("Начинаем конвертацию .vtt файлов в .srt и удаление дубликатов...")
    convert_all_vtt_to_srt_and_cleanup()
    print("Конвертация и очистка завершены. Все `.srt` файлы сохранены в папке 'subtitles'.\n")

    print("Создаём файл с ошибками...")
    write_error_log(failed_numbers)
    print("Процесс завершён.\n")

if __name__ == "__main__":
    main()
