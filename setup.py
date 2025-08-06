#!/usr/bin/env python3
"""
Скрипт для быстрой настройки проекта конвертера медиафайлов
Устанавливает зависимости, настраивает FFmpeg и создает необходимые файлы
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProjectSetup:
    """Класс для настройки проекта"""
    
    def __init__(self):
        self.project_dir = Path.cwd()
        self.system = platform.system().lower()
        
    def check_python_version(self) -> bool:
        """Проверка версии Python"""
        logger.info("🐍 Проверка версии Python...")
        
        if sys.version_info < (3, 7):
            logger.error("❌ Требуется Python 3.7 или выше")
            return False
        
        logger.info(f"✅ Python {sys.version.split()[0]} найден")
        return True
    
    def install_dependencies(self) -> bool:
        """Установка Python зависимостей"""
        logger.info("📦 Установка Python зависимостей...")
        
        try:
            # Обновляем pip
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         capture_output=True, check=True)
            
            # Устанавливаем зависимости
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         capture_output=True, check=True)
            
            logger.info("✅ Зависимости установлены успешно")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Ошибка установки зависимостей: {e}")
            return False
    
    def setup_ffmpeg(self) -> bool:
        """Настройка FFmpeg"""
        logger.info("🎬 Настройка FFmpeg...")
        
        # Проверяем наличие FFmpeg в системе
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("✅ FFmpeg найден в системе")
                return True
        except FileNotFoundError:
            pass
        
        # Проверяем наличие локальной сборки
        local_ffmpeg_paths = [
            "bin/bin/ffmpeg.exe",
            "bin/bin/ffmpeg",
            "ffmpeg.bat",
            "ffmpeg.sh"
        ]
        
        for path in local_ffmpeg_paths:
            if Path(path).exists():
                logger.info(f"✅ Локальная сборка FFmpeg найдена: {path}")
                return True
        
        # Если FFmpeg не найден, предлагаем варианты
        logger.warning("⚠️ FFmpeg не найден")
        logger.info("Варианты установки:")
        logger.info("1. Скачайте с https://ffmpeg.org/ и добавьте в PATH")
        logger.info("2. Запустите: python build_ffmpeg.py (для сборки из исходников)")
        logger.info("3. Используйте пакетный менеджер вашей системы")
        
        return False
    
    def create_sample_files(self):
        """Создание примеров файлов"""
        logger.info("📝 Создание примеров файлов...")
        
        # Создаем папку для примеров
        examples_dir = Path("examples")
        examples_dir.mkdir(exist_ok=True)
        
        # Создаем README для примеров
        examples_readme = """# Примеры использования конвертера

## Запуск GUI конвертера
```bash
python gui_converter.py
```

## Запуск командной строки конвертера
```bash
python convert_media.py "папка_с_файлами" -o "папка_для_сохранения" -q 80
```

## Сборка FFmpeg из исходников
```bash
python build_ffmpeg.py
```

## Поддерживаемые форматы

### Видео
- Входные: MP4, AVI, MOV, MKV, WMV, FLV, WebM
- Выходные: MP4, WebM, AVI, MKV, MOV

### Аудио
- Входные: MP3, WAV, AAC, OGG, FLAC, M4A
- Выходные: MP3, WAV, AAC, OGG, OPUS

### Изображения
- Входные: JPG, PNG, BMP, TIFF, WebP
- Выходные: WebP, JPG, PNG
"""
        
        with open(examples_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(examples_readme)
        
        # Создаем .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
conversion.log
gui_conversion.log

# Build artifacts
build/
bin/
ffmpeg.bat
ffmpeg.sh

# OS
.DS_Store
Thumbs.db

# Project specific
examples/output/
temp/
"""
        
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        
        logger.info("✅ Примеры файлов созданы")
    
    def create_launcher_scripts(self):
        """Создание скриптов запуска"""
        logger.info("🚀 Создание скриптов запуска...")
        
        if self.system == "windows":
            # Создаем batch файлы
            launchers = {
                "run_gui.bat": "@echo off\npython gui_converter.py\npause",
                "run_cli.bat": "@echo off\npython convert_media.py %*\npause",
                "build_ffmpeg.bat": "@echo off\npython build_ffmpeg.py\npause"
            }
        else:
            # Создаем shell скрипты
            launchers = {
                "run_gui.sh": "#!/bin/bash\npython3 gui_converter.py",
                "run_cli.sh": "#!/bin/bash\npython3 convert_media.py \"$@\"",
                "build_ffmpeg.sh": "#!/bin/bash\npython3 build_ffmpeg.py"
            }
        
        for filename, content in launchers.items():
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            # Делаем shell скрипты исполняемыми
            if not self.system == "windows":
                Path(filename).chmod(0o755)
        
        logger.info("✅ Скрипты запуска созданы")
    
    def setup(self) -> bool:
        """Полная настройка проекта"""
        logger.info("🚀 Начинаем настройку проекта...")
        
        # Проверяем Python
        if not self.check_python_version():
            return False
        
        # Устанавливаем зависимости
        if not self.install_dependencies():
            return False
        
        # Настраиваем FFmpeg
        self.setup_ffmpeg()
        
        # Создаем примеры файлов
        self.create_sample_files()
        
        # Создаем скрипты запуска
        self.create_launcher_scripts()
        
        logger.info("🎉 Настройка проекта завершена!")
        logger.info("\n📋 Что дальше:")
        logger.info("1. Запустите GUI: python gui_converter.py")
        logger.info("2. Или используйте CLI: python convert_media.py --help")
        logger.info("3. Если FFmpeg не найден, установите его или соберите из исходников")
        
        return True

def main():
    """Главная функция"""
    setup = ProjectSetup()
    
    if setup.setup():
        print("\n✅ Проект успешно настроен!")
        print("Теперь вы можете использовать конвертер медиафайлов.")
    else:
        print("\n❌ Ошибка настройки проекта")
        print("Проверьте логи выше для получения дополнительной информации.")

if __name__ == '__main__':
    main() 