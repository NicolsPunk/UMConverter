#!/usr/bin/env python3
"""
Скрипт для скачивания готовой сборки FFmpeg для Windows
Альтернатива сборке из исходников
"""

import os
import sys
import subprocess
import platform
import zipfile
import requests
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FFmpegDownloader:
    """Класс для скачивания FFmpeg"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.bin_dir = Path("bin")
        self.ffmpeg_dir = self.bin_dir / "ffmpeg"
        
    def check_system(self) -> bool:
        """Проверка системы"""
        if self.system != "windows":
            logger.error("❌ Этот скрипт предназначен только для Windows")
            logger.info("💡 Для Linux/macOS используйте: python build_ffmpeg.py")
            return False
        return True
    
    def get_ffmpeg_url(self) -> str:
        """Получение URL для скачивания FFmpeg"""
        # Используем официальные сборки от BtbN
        base_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest"
        
        # Определяем архитектуру
        if platform.machine().endswith('64'):
            arch = "win64"
        else:
            arch = "win32"
        
        filename = f"ffmpeg-master-latest-{arch}-gpl.zip"
        return f"{base_url}/{filename}"
    
    def download_ffmpeg(self) -> bool:
        """Скачивание FFmpeg"""
        try:
            url = self.get_ffmpeg_url()
            filename = url.split('/')[-1]
            download_path = Path(filename)
            
            logger.info(f"📥 Скачивание FFmpeg с {url}")
            logger.info(f"📁 Файл: {filename}")
            
            # Скачиваем файл
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Показываем прогресс
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            logger.info(f"📊 Прогресс: {progress:.1f}%")
            
            logger.info("✅ Скачивание завершено")
            return self.extract_ffmpeg(download_path)
            
        except Exception as e:
            logger.error(f"❌ Ошибка скачивания: {e}")
            return False
    
    def extract_ffmpeg(self, zip_path: Path) -> bool:
        """Распаковка FFmpeg"""
        try:
            logger.info("📦 Распаковка FFmpeg...")
            
            # Создаем папку bin если её нет
            self.bin_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.bin_dir)
            
            # Находим папку с FFmpeg
            ffmpeg_folders = list(self.bin_dir.glob("ffmpeg-*"))
            if ffmpeg_folders:
                ffmpeg_folder = ffmpeg_folders[0]
                # Переименовываем в ffmpeg
                ffmpeg_folder.rename(self.ffmpeg_dir)
                logger.info(f"✅ FFmpeg распакован в {self.ffmpeg_dir}")
            else:
                logger.error("❌ Не удалось найти папку с FFmpeg в архиве")
                return False
            
            # Удаляем zip файл
            zip_path.unlink()
            logger.info("🗑️ Временный файл удален")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка распаковки: {e}")
            return False
    
    def create_wrapper_script(self):
        """Создание скрипта-обертки"""
        logger.info("📝 Создание скрипта-обертки...")
        
        # Путь к исполняемым файлам
        bin_path = self.ffmpeg_dir / "bin"
        
        if not bin_path.exists():
            logger.error("❌ Папка bin не найдена в распакованном FFmpeg")
            return False
        
        # Создаем batch файл
        wrapper_content = f"""@echo off
set FFMPEG_PATH=%~dp0{self.ffmpeg_dir}\\bin
set PATH=%FFMPEG_PATH%;%PATH%
ffmpeg.exe %*
"""
        
        wrapper_path = Path("ffmpeg.bat")
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_content)
        
        logger.info(f"✅ Скрипт-обертка создан: {wrapper_path}")
        return True
    
    def test_ffmpeg(self) -> bool:
        """Тестирование FFmpeg"""
        try:
            logger.info("🧪 Тестирование FFmpeg...")
            
            # Пробуем запустить ffmpeg
            ffmpeg_exe = self.ffmpeg_dir / "bin" / "ffmpeg.exe"
            if not ffmpeg_exe.exists():
                logger.error("❌ ffmpeg.exe не найден")
                return False
            
            result = subprocess.run([str(ffmpeg_exe), "-version"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ FFmpeg работает корректно")
                return True
            else:
                logger.error(f"❌ Ошибка запуска FFmpeg: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ошибка тестирования: {e}")
            return False
    
    def download(self) -> bool:
        """Полный процесс скачивания"""
        logger.info("🚀 Начинаем скачивание FFmpeg...")
        
        # Проверяем систему
        if not self.check_system():
            return False
        
        # Скачиваем FFmpeg
        if not self.download_ffmpeg():
            return False
        
        # Создаем скрипт-обертку
        if not self.create_wrapper_script():
            return False
        
        # Тестируем FFmpeg
        if not self.test_ffmpeg():
            return False
        
        logger.info("🎉 Скачивание FFmpeg завершено успешно!")
        logger.info(f"📁 FFmpeg установлен в: {self.ffmpeg_dir}")
        logger.info("🔧 Используйте ffmpeg.bat для запуска")
        
        return True

def main():
    """Главная функция"""
    downloader = FFmpegDownloader()
    
    if downloader.download():
        print("\n✅ FFmpeg успешно скачан и установлен!")
        print("Теперь вы можете использовать локальную версию FFmpeg в вашем проекте.")
    else:
        print("\n❌ Ошибка скачивания FFmpeg")
        print("Проверьте логи выше для получения дополнительной информации.")

if __name__ == '__main__':
    main()