import os
import sys

def main():
    # Получаем директорию скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Получаем имя самого скрипта
    script_name = os.path.basename(__file__)
    
    # Запрашиваем у пользователя количество букв для удаления
    while True:
        try:
            n = int(input("Введите количество первых букв, которые нужно удалить из имен файлов: "))
            if n < 0:
                print("Пожалуйста, введите неотрицательное число.")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое число.")
    
    # Получаем список файлов в директории, исключая сам скрипт
    files = [
        f for f in os.listdir(script_dir)
        if os.path.isfile(os.path.join(script_dir, f)) and f != script_name
    ]
    
    if not files:
        print("В папке нет других файлов для переименования.")
        return
    
    # Предварительный просмотр изменений
    print("\nСписок файлов, которые будут изменены:")
    for f in files:
        if len(f) > n:
            new_name = f[n:]
            print(f"{f} --> {new_name}")
        else:
            print(f"{f} --> (Имя короче {n} символов, пропущено)")
    
    # Запрашиваем подтверждение
    confirmation = input("\nВы уверены, что хотите продолжить? Это действие необратимо! (да/нет): ").strip().lower()
    if confirmation != 'да':
        print("Операция отменена.")
        return
    
    # Переименовываем файлы
    for f in files:
        old_path = os.path.join(script_dir, f)
        if len(f) > n:
            new_name = f[n:]
            new_path = os.path.join(script_dir, new_name)
            try:
                # Проверяем, не существует ли уже файл с новым именем
                if os.path.exists(new_path):
                    print(f"Не удалось переименовать {f}: файл с именем {new_name} уже существует.")
                    continue
                os.rename(old_path, new_path)
                print(f"Переименован: {f} --> {new_name}")
            except Exception as e:
                print(f"Не удалось переименовать {f}: {e}")
        else:
            print(f"Пропущен файл {f} (имя короче {n} символов).")
    
    print("\nГотово.")

if __name__ == "__main__":
    main()
