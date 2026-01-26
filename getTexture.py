import os
import sys
from PIL import Image
from pathlib import Path

def scale_images_in_folder(folder_path, scale_factor=3):
    """
    Увеличивает все изображения в папке в scale_factor^2 раз (scale_factor по ширине и высоте)
    с использованием NEAREST фильтра для сохранения пиксельности
    """
    # Поддерживаемые форматы изображений
    supported_formats = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tga', '.tiff'}
    
    # Преобразуем путь к абсолютному
    folder_path = Path(folder_path).absolute()
    
    # Проверяем, существует ли папка
    if not folder_path.exists():
        print(f"Ошибка: Папка '{folder_path}' не существует!")
        return
    
    print(f"Обработка папки: {folder_path}")
    print(f"Коэффициент увеличения: {scale_factor}x (итого в {scale_factor*scale_factor} раз)")
    
    # Создаем подпапку для результатов
    output_folder = folder_path / "scaled_x9"
    output_folder.mkdir(exist_ok=True)
    
    # Счетчики
    processed = 0
    skipped = 0
    errors = 0
    
    # Проходим по всем файлам в папке
    for file_path in folder_path.iterdir():
        # Пропускаем подпапки
        if file_path.is_dir():
            continue
            
        # Проверяем расширение файла
        if file_path.suffix.lower() not in supported_formats:
            continue
            
        try:
            # Открываем изображение
            with Image.open(file_path) as img:
                # Конвертируем в RGBA для сохранения прозрачности
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGBA')
                
                # Получаем оригинальные размеры
                original_width, original_height = img.size
                
                # Вычисляем новые размеры (увеличиваем в scale_factor раз)
                new_width = original_width * scale_factor
                new_height = original_height * scale_factor
                
                # Увеличиваем изображение с использованием NEAREST фильтра (без сглаживания)
                scaled_img = img.resize(
                    (new_width, new_height),
                    resample=Image.NEAREST  # или Image.Resampling.NEAREST для Pillow >= 9.1.0
                )
                
                # Формируем имя для сохранения
                output_filename = f"{file_path.stem}_x{scale_factor}{file_path.suffix}"
                output_path = output_folder / output_filename
                
                # Сохраняем изображение
                if file_path.suffix.lower() in ['.jpg', '.jpeg']:
                    # Для JPEG сохраняем без альфа-канала
                    scaled_img.convert('RGB').save(output_path, quality=95)
                else:
                    # Для других форматов сохраняем как есть
                    scaled_img.save(output_path)
                
                print(f"✓ {file_path.name} ({original_width}x{original_height}) → "
                      f"{output_filename} ({new_width}x{new_height})")
                processed += 1
                
        except Exception as e:
            print(f"✗ Ошибка при обработке {file_path.name}: {e}")
            errors += 1
    
    # Выводим статистику
    print("\n" + "="*50)
    print("Обработка завершена!")
    print(f"Обработано файлов: {processed}")
    print(f"Пропущено файлов: {skipped}")
    print(f"Ошибок: {errors}")
    print(f"Результаты сохранены в: {output_folder}")
    
    # Если обработан хотя бы один файл, открываем папку с результатами
    if processed > 0:
        try:
            # Для Windows
            if sys.platform == 'win32':
                os.startfile(output_folder)
            # Для macOS
            elif sys.platform == 'darwin':
                os.system(f'open "{output_folder}"')
            # Для Linux
            else:
                os.system(f'xdg-open "{output_folder}"')
        except:
            pass
def main():
    """Основная функция скрипта"""
    print("="*50)
    print("УВЕЛИЧИТЕЛЬ ТЕКСТУР В 9 РАЗ")
    print("="*50)
    print("Этот скрипт увеличивает все изображения в указанной папке")
    print("в 9 раз (3х по ширине и 3х по высоте) без сглаживания")
    print("="*50)
    
    while True:
        try:
            # Запрашиваем путь к папке
            user_input = input("\nВведите путь к папке с текстурами (или 'q' для выхода): ").strip()
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                print("Выход из программы.")
                break
            
            if not user_input:
                print("❌ Путь не может быть пустым!")
                continue
            
            # Обрабатываем путь
            folder_path = Path(user_input)
            
            # Проверяем путь
            if not folder_path.exists():
                print(f"❌ Указанный путь не существует: {folder_path}")
                continue
            
            if not folder_path.is_dir():
                print(f"❌ Указанный путь не является папкой: {folder_path}")
                continue
            
            # Уточняем коэффициент масштабирования
            print("\n" + "-"*50)
            print("Выберите коэффициент масштабирования:")
            print("1) Увеличить в 4 раза (2x2)")
            print("2) Увеличить в 9 раз (3x3) - по умолчанию")
            print("3) Увеличить в 16 раз (4x4)")
            print("4) Увеличить в 25 раз (5x5)")
            
            scale_choice = input("\nВаш выбор (1-4, по умолчанию 2): ").strip()
            
            scale_factors = {
                '1': 2,
                '2': 3,
                '3': 4,
                '4': 5
            }
            
            scale_factor = scale_factors.get(scale_choice, 3)
            
            # Подтверждение
            confirm = input(f"\nУвеличить все изображения в папке '{folder_path.name}' "
                          f"в {scale_factor*scale_factor} раз ({scale_factor}x{scale_factor})? (y/N): ")
            
            if confirm.lower() not in ['y', 'yes', 'д', 'да']:
                print("Отменено пользователем.")
                continue
            
            # Запускаем обработку
            scale_images_in_folder(folder_path, scale_factor)
            
            # Спрашиваем, хотим ли обработать другую папку
            again = input("\nОбработать другую папку? (y/N): ")
            if again.lower() not in ['y', 'yes', 'д', 'да']:
                print("Выход из программы.")
                break
                
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    # Проверяем, установлен ли Pillow
    try:
        from PIL import Image
    except ImportError:
        print("❌ Для работы скрипта требуется библиотека Pillow!")
        print("Установите её командой: pip install pillow")
        sys.exit(1)
    
    main()