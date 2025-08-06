#!/usr/bin/env python3
"""
Скрипт для конвертации изображений в WebP и видео в WebM
Поддерживает форматы: PNG, JPG, JPEG, BMP, TIFF -> WebP
Поддерживает форматы: MP4, AVI, MOV, MKV -> WebM
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple
import subprocess
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MediaConverter:
    def __init__(self, input_dir: str, output_dir: str = None, quality: int = 80):
        """
        Инициализация конвертера
        
        Args:
            input_dir: Папка с исходными файлами
            output_dir: Папка для сохранения конвертированных файлов (по умолчанию та же)
            quality: Качество сжатия (1-100)
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) if output_dir else self.input_dir
        self.quality = quality
        
        # Создаем папку для выходных файлов, если её нет
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Поддерживаемые форматы изображений
        self.image_formats = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
        
        # Поддерживаемые форматы видео
        self.video_formats = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}
        
        logger.info(f"Конвертер инициализирован:")
        logger.info(f"  Входная папка: {self.input_dir}")
        logger.info(f"  Выходная папка: {self.output_dir}")
        logger.info(f"  Качество: {self.quality}")

    def check_dependencies(self) -> bool:
        """Проверка наличия необходимых зависимостей"""
        try:
            # Проверяем Pillow для изображений
            import PIL
            logger.info("Pillow найден для обработки изображений")
        except ImportError:
            logger.error("Pillow не установлен. Установите: pip install Pillow")
            return False
        
        try:
            # Проверяем ffmpeg для видео
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("FFmpeg найден для обработки видео")
            else:
                logger.error("FFmpeg не найден или не работает")
                return False
        except FileNotFoundError:
            logger.error("FFmpeg не установлен. Скачайте с https://ffmpeg.org/")
            return False
        
        return True

    def find_files(self, extensions: set) -> List[Path]:
        """Поиск файлов с указанными расширениями"""
        files = []
        for ext in extensions:
            files.extend(self.input_dir.glob(f"*{ext}"))
            files.extend(self.input_dir.glob(f"*{ext.upper()}"))
        return files

    def convert_image_to_webp(self, input_path: Path) -> bool:
        """
        Конвертация изображения в WebP
        
        Args:
            input_path: Путь к исходному файлу
            
        Returns:
            bool: True если конвертация успешна
        """
        try:
            from PIL import Image
            
            # Открываем изображение
            with Image.open(input_path) as img:
                # Конвертируем в RGB если нужно
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Создаем белый фон для прозрачных изображений
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Формируем имя выходного файла
                output_path = self.output_dir / f"{input_path.stem}.webp"
                
                # Сохраняем в WebP
                img.save(output_path, 'WEBP', quality=self.quality, method=6)
                
                # Получаем размеры файлов
                input_size = input_path.stat().st_size
                output_size = output_path.stat().st_size
                compression_ratio = (1 - output_size / input_size) * 100
                
                logger.info(f"✅ {input_path.name} -> {output_path.name}")
                logger.info(f"   Размер: {input_size / 1024:.1f}KB -> {output_size / 1024:.1f}KB")
                logger.info(f"   Сжатие: {compression_ratio:.1f}%")
                
                return True
                
        except Exception as e:
            logger.error(f"❌ Ошибка конвертации {input_path.name}: {str(e)}")
            return False

    def convert_video_to_webm(self, input_path: Path) -> bool:
        """
        Конвертация видео в WebM
        
        Args:
            input_path: Путь к исходному файлу
            
        Returns:
            bool: True если конвертация успешна
        """
        try:
            # Формируем имя выходного файла
            output_path = self.output_dir / f"{input_path.stem}.webm"
            
            # Команда для FFmpeg
            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                '-c:v', 'libvpx-vp9',  # Видеокодек VP9
                '-c:a', 'libopus',      # Аудиокодек Opus
                '-crf', '30',           # Качество (0-63, чем меньше тем лучше)
                '-b:v', '0',            # Переменный битрейт
                '-deadline', 'good',     # Скорость кодирования
                '-cpu-used', '2',       # Использование CPU
                '-auto-alt-ref', '0',   # Отключаем альтернативные ссылки
                '-f', 'webm',           # Формат вывода
                '-y',                   # Перезаписывать существующие файлы
                str(output_path)
            ]
            
            # Запускаем конвертацию
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Получаем размеры файлов
                input_size = input_path.stat().st_size
                output_size = output_path.stat().st_size
                compression_ratio = (1 - output_size / input_size) * 100
                
                logger.info(f"✅ {input_path.name} -> {output_path.name}")
                logger.info(f"   Размер: {input_size / 1024 / 1024:.1f}MB -> {output_size / 1024 / 1024:.1f}MB")
                logger.info(f"   Сжатие: {compression_ratio:.1f}%")
                
                return True
            else:
                logger.error(f"❌ Ошибка FFmpeg для {input_path.name}: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ошибка конвертации {input_path.name}: {str(e)}")
            return False

    def convert_images(self) -> Tuple[int, int]:
        """Конвертация всех изображений в WebP"""
        image_files = self.find_files(self.image_formats)
        
        if not image_files:
            logger.info("Изображения для конвертации не найдены")
            return 0, 0
        
        logger.info(f"Найдено {len(image_files)} изображений для конвертации")
        
        successful = 0
        failed = 0
        
        for image_file in image_files:
            if self.convert_image_to_webp(image_file):
                successful += 1
            else:
                failed += 1
        
        return successful, failed

    def convert_videos(self) -> Tuple[int, int]:
        """Конвертация всех видео в WebM"""
        video_files = self.find_files(self.video_formats)
        
        if not video_files:
            logger.info("Видео для конвертации не найдены")
            return 0, 0
        
        logger.info(f"Найдено {len(video_files)} видео для конвертации")
        
        successful = 0
        failed = 0
        
        for video_file in video_files:
            if self.convert_video_to_webm(video_file):
                successful += 1
            else:
                failed += 1
        
        return successful, failed

    def run(self, convert_images: bool = True, convert_videos: bool = True):
        """
        Запуск конвертации
        
        Args:
            convert_images: Конвертировать изображения
            convert_videos: Конвертировать видео
        """
        logger.info("🚀 Начинаем конвертацию медиафайлов...")
        
        # Проверяем зависимости
        if not self.check_dependencies():
            logger.error("❌ Зависимости не найдены. Прерываем конвертацию.")
            return
        
        total_successful = 0
        total_failed = 0
        
        # Конвертируем изображения
        if convert_images:
            logger.info("📸 Конвертация изображений...")
            img_success, img_failed = self.convert_images()
            total_successful += img_success
            total_failed += img_failed
        
        # Конвертируем видео
        if convert_videos:
            logger.info("🎬 Конвертация видео...")
            vid_success, vid_failed = self.convert_videos()
            total_successful += vid_success
            total_failed += vid_failed
        
        # Итоговый отчет
        logger.info("📊 Итоговый отчет:")
        logger.info(f"   Успешно конвертировано: {total_successful}")
        logger.info(f"   Ошибок: {total_failed}")
        logger.info(f"   Всего обработано: {total_successful + total_failed}")
        
        if total_failed == 0:
            logger.info("🎉 Все файлы успешно конвертированы!")
        else:
            logger.warning(f"⚠️  {total_failed} файлов не удалось конвертировать")


def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description='Конвертер изображений в WebP и видео в WebM')
    parser.add_argument('input_dir', help='Папка с исходными файлами')
    parser.add_argument('-o', '--output', help='Папка для сохранения (по умолчанию та же)')
    parser.add_argument('-q', '--quality', type=int, default=80, 
                       help='Качество WebP (1-100, по умолчанию 80)')
    parser.add_argument('--images-only', action='store_true', 
                       help='Конвертировать только изображения')
    parser.add_argument('--videos-only', action='store_true', 
                       help='Конвертировать только видео')
    
    args = parser.parse_args()
    
    # Проверяем существование входной папки
    if not os.path.exists(args.input_dir):
        logger.error(f"Папка {args.input_dir} не существует")
        sys.exit(1)
    
    # Создаем конвертер
    converter = MediaConverter(args.input_dir, args.output, args.quality)
    
    # Определяем что конвертировать
    convert_images = not args.videos_only
    convert_videos = not args.images_only
    
    # Запускаем конвертацию
    converter.run(convert_images, convert_videos)


if __name__ == '__main__':
    main() 