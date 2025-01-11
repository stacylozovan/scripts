import yt_dlp
import os
import re
import subprocess
import sys

def check_ffmpeg_installed():
    """
    Проверяет, установлен ли ffmpeg и доступен ли он в PATH.
    Если ffmpeg не найден — выводит инструкцию и ждёт нажатия Enter, затем завершает работу.
    """
    try:
        subprocess.run(
            ['ffmpeg', '-version'],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        print("Похоже, что ffmpeg не установлен или не добавлен в PATH.\n")
        print("Как установить ffmpeg (Windows):")
        print("1. Скачайте архив с ffmpeg по ссылке: https://ffmpeg.org/download.html")
        print("2. Распакуйте архив в удобную папку, например C:\\ffmpeg\\bin")
        print("3. Добавьте путь к bin (например, C:\\ffmpeg\\bin) в переменную окружения PATH.\n")
        input("Нажмите Enter, чтобы выйти...")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("ffmpeg установлен, но возникла ошибка при его вызове.")
        input("Нажмите Enter, чтобы выйти...")
        sys.exit(1)

def get_playlist_info(playlist_url):
    """
    Возвращает кортеж (total_videos, first_video_url) для заданного плейлиста.
    Если не удалось извлечь информацию — возвращает (0, None).
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,  # Получаем базовую информацию о списке
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=False)
        if 'entries' not in info_dict or not info_dict['entries']:
            print("Не удалось извлечь информацию о плейлисте (он пуст или недоступен).")
            return (0, None)
    except Exception as e:
        print(f"Ошибка при извлечении информации о плейлисте: {e}")
        return (0, None)

    total_videos = len(info_dict['entries'])
    first_video = info_dict['entries'][0]
    # 'url' может меняться в зависимости от структуры,
    # но в extract_flat обычно это поле называется 'url'
    first_video_url = first_video['url']

    return (total_videos, first_video_url)

def list_available_formats(video_url):
    """
    Выводит на экран список форматов/качеств для примера видео (обычно первое из плейлиста).
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'listformats': True,
    }
    print("Список доступных форматов (кодек + разрешение):\n")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(video_url, download=False)
    except Exception as e:
        print(f"Не удалось получить список форматов: {e}")

def download_video(playlist_url, desired_resolution='720p'):
    """
    Скачивает все видео из плейлиста в лучшем доступном формате, 
    но с ограничением по разрешению (bestvideo[height<=...]) + bestaudio.
    Файлы нумеруются (001, 002, ...) и сохраняются в папку "Video".
    """
    save_dir = 'Video'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Числовое значение разрешения, чтобы получить, например, 720 из '720p'
    resolution_number = ''.join(filter(str.isdigit, desired_resolution))

    # Если разрешение не получилось извлечь, по умолчанию 720
    if not resolution_number.isdigit():
        resolution_number = "720"

    # Формат с fallback:
    # 1) bestvideo высотой <= resolution_number + bestaudio
    # 2) если не получилось, best
    ydl_format = (
        f"bestvideo[height<={resolution_number}]+bestaudio/best"
    )

    ydl_opts = {
        'ignoreerrors': True,  # Не прерывать скачивание при ошибке в одном видео
        'outtmpl': os.path.join(save_dir, '%(playlist_index)03d.%(title)s.%(ext)s'),
        'format': ydl_format,
        'playlistend': 5000,   # Чтобы скачивались все видео плейлиста до 5000
    }

    failed_numbers = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            if 'entries' not in playlist_info:
                print("Не удалось извлечь информацию о плейлисте.")
                return []
            total_videos = len(playlist_info['entries'])
            print(f"\nНачинаем загрузку видео... Всего видео: {total_videos}\n")
            ydl.download([playlist_url])

        # Проверяем, какие видео не скачались
        for i in range(1, total_videos + 1):
            number_str = f"{i:03d}"
            # Файлы могут иметь разные расширения (mp4, mkv, webm...)
            pattern = re.compile(rf'^{number_str}\..*\.(mp4|mkv|webm|flv|mov|avi)$', re.IGNORECASE)
            found = [f for f in os.listdir(save_dir) if pattern.match(f)]
            if not found:
                failed_numbers.append(number_str)
                print(f"Видео не найдено для номера: {number_str}")

    except Exception as e:
        print(f"Ошибка при загрузке видео: {e}")

    return failed_numbers

def download_audio(playlist_url):
    """
    Скачивает лучшие аудио-дорожки (bestaudio) из плейлиста.
    Файлы нумеруются и сохраняются в папку "Audio".
    """
    save_dir = 'Audio'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    ydl_opts = {
        'ignoreerrors': True,
        'outtmpl': os.path.join(save_dir, '%(playlist_index)03d.%(title)s.%(ext)s'),
        # bestaudio автоматом выберет лучший вариант аудио, обычно m4a/webm
        'format': 'bestaudio/best',
        'playlistend': 5000,
    }

    failed_numbers = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            if 'entries' not in playlist_info:
                print("Не удалось извлечь информацию о плейлисте.")
                return []
            total_videos = len(playlist_info['entries'])
            print(f"\nНачинаем загрузку аудио... Всего треков: {total_videos}\n")
            ydl.download([playlist_url])

        # Проверяем, какие аудио не скачались
        for i in range(1, total_videos + 1):
            number_str = f"{i:03d}"
            # Наиболее распространённые расширения аудио
            pattern = re.compile(rf'^{number_str}\..*\.(m4a|webm|mp3|opus|aac|wav|flac)$', re.IGNORECASE)
            found = [f for f in os.listdir(save_dir) if pattern.match(f)]
            if not found:
                failed_numbers.append(number_str)
                print(f"Аудио не найдено для номера: {number_str}")

    except Exception as e:
        print(f"Ошибка при загрузке аудио: {e}")

    return failed_numbers

def write_error_log(missing_numbers, error_file_path='errors.txt'):
    """
    Записывает список неудавшихся номеров в файл с ошибками.
    """
    total_failures = len(missing_numbers)
    if total_failures == 0:
        print("Все файлы были успешно скачаны.")
        return

    with open(error_file_path, 'w', encoding='utf-8') as error_file:
        error_file.write("Список номеров, для которых не удалось скачать файл:\n\n")
        for number in missing_numbers:
            error_file.write(f"{number}\n")
        error_file.write(f"\nОбщее количество неудачных попыток: {total_failures}\n")

    print(f"Файл с ошибками создан: {error_file_path}")
    print(f"Всего неудачных попыток: {total_failures}")

def main():
    check_ffmpeg_installed()

    playlist_link = input("Введите ссылку на плейлист YouTube: ").strip()
    if not playlist_link:
        print("Ссылка не может быть пустой. Завершение работы.")
        input("Нажмите Enter, чтобы выйти...")
        return

    total_videos, first_video_url = get_playlist_info(playlist_link)
    if total_videos == 0:
        print("Не удалось определить количество видео в плейлисте. Завершение работы.")
        input("Нажмите Enter, чтобы выйти...")
        return
    else:
        print(f"В плейлисте обнаружено видео: {total_videos} шт.\n")

    # Показываем форматы для примера (первого видео)
    print("Доступные форматы и разрешения для первого видео:\n")
    list_available_formats(first_video_url)

    # Спрашиваем, что качать: аудио или видео
    print("\nЧто вы хотите скачать?")
    print("1. Видео")
    print("2. Аудио")
    choice = input("Введите номер (1 или 2): ").strip()

    failed_numbers = []

    if choice == '1':
        # Если видео — спрашиваем желаемое разрешение
        print("\nВведите желаемое разрешение (например: 1080p, 720p, 480p, 360p).")
        desired_resolution = input("Укажите разрешение: ").strip()
        if not desired_resolution:
            desired_resolution = "720p"  # По умолчанию
        failed_numbers = download_video(playlist_link, desired_resolution)
    elif choice == '2':
        # Скачиваем аудио
        failed_numbers = download_audio(playlist_link)
    else:
        print("Неверный выбор. Завершение работы.")
        input("Нажмите Enter, чтобы выйти...")
        return

    print("\nСкачивание завершено. Проверяем ошибки...")
    write_error_log(failed_numbers)

    # Чтобы окно не закрылось моментально
    input("Нажмите Enter, чтобы выйти...")

if __name__ == "__main__":
    main()
