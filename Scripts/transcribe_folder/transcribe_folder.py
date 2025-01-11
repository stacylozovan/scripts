import os
import wave
import json
from vosk import Model, KaldiRecognizer
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def create_directory(path):
    """
    Создаёт директорию, если её не существует.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def convert_audio(input_path, output_path):
    """
    Преобразует аудио в формат WAV 16kHz моно
    """
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")

def transcribe_audio_vosk(audio_path, model_path):
    """
    Распознаёт речь из аудиофайла с использованием Vosk.
    """
    try:
        if not os.path.exists(model_path):
            return "Модель не найдена. Проверьте путь."

        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 16000)

        with wave.open(audio_path, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
                return "Аудиофайл должен быть в формате WAV с частотой 16kHz и моно."

            transcription = ""
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    transcription += result.get("text", "") + "\n"

            final_result = json.loads(recognizer.FinalResult())
            transcription += final_result.get("text", "") + "\n"

        return transcription.strip()
    except Exception as e:
        return f"Ошибка при распознавании аудио: {e}"

def process_video(video_path, model_path, temp_dir, output_dir):
    """
    Извлекает аудио из видео, преобразует и распознаёт речь.
    """
    try:
        temp_audio_path = os.path.join(temp_dir, "temp_audio.wav")
        raw_audio_path = os.path.join(temp_dir, "temp_audio_raw.wav")

        video = VideoFileClip(video_path)
        video.audio.write_audiofile(raw_audio_path, codec="pcm_s16le")

        convert_audio(raw_audio_path, temp_audio_path)

        transcription = transcribe_audio_vosk(temp_audio_path, model_path)

        text_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(video_path))[0] + ".txt")
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(transcription)

        return f"Обработка завершена: {video_path} -> {text_file_path}"

    except Exception as e:
        return f"Ошибка при обработке файла {video_path}: {e}"

    finally:
        if os.path.exists(raw_audio_path):
            os.remove(raw_audio_path)
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

def process_videos_in_folder(folder_path, model_path, temp_dir, output_dir):
    """
    Обрабатывает все видеофайлы в папке параллельно.
    """
    create_directory(temp_dir)
    create_directory(output_dir)

    video_extensions = (".mp4", ".avi", ".mov", ".mkv", ".webm")
    video_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(video_extensions)]

    if not video_files:
        print("В папке нет видеофайлов.")
        return

    results = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_video, video, model_path, temp_dir, output_dir) for video in video_files]

        for future in tqdm(futures, desc="Обработка видео"):
            results.append(future.result())

    for result in results:
        print(result)

if __name__ == "__main__":
    current_folder = os.getcwd()
    model_path = "C:\\models\\!vosk!\\vosk-model-ru-0.42"
    temp_dir = os.path.join(current_folder, "temp_files")
    output_dir = os.path.join(current_folder, "transcriptions")

    print(f"Скрипт ищет видеофайлы в папке: {current_folder}")
    process_videos_in_folder(current_folder, model_path, temp_dir, output_dir)
