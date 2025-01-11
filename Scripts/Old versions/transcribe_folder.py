import os
import wave
import json
from vosk import Model, KaldiRecognizer
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def convert_audio(input_path, output_path):
    """
    Преобразует аудио в формат WAV 16kHz моно
    """
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")

def transcribe_audio_vosk(audio_path, model_path="C:\\models\\!vosk!\\vosk-model-ru-0.42"):
    """
    Распознаёт речь из аудиофайла с использованием Vosk, отображая прогресс в процентах.
    """
    if not os.path.exists(model_path):
        return "Модель не найдена. Проверьте путь."

    # Загрузка модели
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    # Открываем аудиофайл
    with wave.open(audio_path, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            return "Аудиофайл должен быть в формате WAV с частотой 16kHz и моно."

        transcription = ""
        total_frames = wf.getnframes()
        frame_step = 4000
        processed_frames = 0

        while True:
            data = wf.readframes(frame_step)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if "text" in result:
                    clean_text = result["text"].replace("\\\"", "").strip()
                    transcription += clean_text + "\n\n"

            # Обновляем прогресс
            processed_frames += frame_step
            progress = min(100, int(processed_frames / total_frames * 100))
            print(f"Прогресс: {progress}%", end="\r")

        # Финальный результат
        final_result = json.loads(recognizer.FinalResult())
        if "text" in final_result:
            clean_text = final_result["text"].replace("\\\"", "").strip()
            transcription += clean_text + "\n\n"

    print("Прогресс: 100%")
    return transcription

def process_video(video_path, model_path="C:\\models\\!vosk!\\vosk-model-ru-0.42"):
    """
    Извлекает аудио из видео, преобразует и распознаёт речь
    """
    audio_path = "temp_audio.wav"
    try:
        # Извлечение аудио из видео
        video = VideoFileClip(video_path)
        video.audio.write_audiofile("temp_audio_raw.wav", codec="pcm_s16le")

        # Конвертация аудио в формат WAV 16kHz моно
        convert_audio("temp_audio_raw.wav", audio_path)

        # Распознавание речи
        transcription = transcribe_audio_vosk(audio_path, model_path)

    finally:
        # Удаление временных файлов
        if os.path.exists("temp_audio_raw.wav"):
            os.remove("temp_audio_raw.wav")
        if os.path.exists(audio_path):
            os.remove(audio_path)

    return transcription

def process_videos_in_folder(folder_path, model_path="C:\\models\\!vosk!\\vosk-model-ru-0.42"):
    """
    Обрабатывает все видеофайлы в папке, распознаёт речь и сохраняет результат в текстовые файлы
    """
    video_extensions = (".mp4", ".avi", ".mov", ".mkv", ".webm")
    video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(video_extensions)]

    if not video_files:
        print("В папке нет видеофайлов.")
        return

    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        print(f"Обработка видео: {video_file}")
        transcription = process_video(video_path, model_path)

        # Сохранение транскрипции в текстовый файл
        text_file_path = os.path.splitext(video_path)[0] + ".txt"
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(transcription.strip())
        print(f"Транскрипция сохранена в: {text_file_path}")

if __name__ == "__main__":
    current_folder = os.getcwd()
    print(f"Скрипт ищет видеофайлы в папке: {current_folder}")
    process_videos_in_folder(current_folder)
