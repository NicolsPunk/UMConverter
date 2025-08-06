#!/usr/bin/env python3
"""
Универсальный установщик для конвертера медиафайлов
Universal installer for media converter
"""

import os
import sys
import subprocess
import platform
import zipfile
import requests
from pathlib import Path
import logging
import json
import locale

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Localization:
    """Класс для локализации"""
    
    def __init__(self):
        self.current_lang = self._detect_language()
        self.translations = {
            'ru': {
                'title': '🎬 Установщик конвертера медиафайлов',
                'checking_python': '🐍 Проверка версии Python...',
                'python_version_error': '❌ Требуется Python 3.7 или выше',
                'python_found': '✅ Python {} найден',
                'installing_deps': '📦 Установка Python зависимостей...',
                'deps_install_error': '❌ Ошибка установки зависимостей: {}',
                'deps_installed': '✅ Зависимости установлены успешно',
                'ffmpeg_setup': '🎬 Настройка FFmpeg...',
                'ffmpeg_found_system': '✅ FFmpeg найден в системе',
                'ffmpeg_found_local': '✅ Локальная сборка FFmpeg найдена: {}',
                'ffmpeg_not_found': '⚠️ FFmpeg не найден',
                'ffmpeg_options': 'Варианты установки:',
                'ffmpeg_option1': '1. Скачайте с https://ffmpeg.org/ и добавьте в PATH',
                'ffmpeg_option2': '2. Автоматическая установка (рекомендуется)',
                'ffmpeg_option3': '3. Используйте пакетный менеджер вашей системы',
                'downloading_ffmpeg': '📥 Скачивание FFmpeg...',
                'ffmpeg_download_error': '❌ Ошибка скачивания: {}',
                'ffmpeg_downloaded': '✅ Скачивание завершено',
                'extracting_ffmpeg': '📦 Распаковка FFmpeg...',
                'ffmpeg_extract_error': '❌ Ошибка распаковки: {}',
                'ffmpeg_extracted': '✅ FFmpeg распакован в {}',
                'temp_file_deleted': '🗑️ Временный файл удален',
                'creating_wrapper': '📝 Создание скрипта-обертки...',
                'wrapper_created': '✅ Скрипт-обертка создан: {}',
                'testing_ffmpeg': '🧪 Тестирование FFmpeg...',
                'ffmpeg_test_error': '❌ Ошибка тестирования: {}',
                'ffmpeg_works': '✅ FFmpeg работает корректно',
                'creating_samples': '📝 Создание примеров файлов...',
                'samples_created': '✅ Примеры файлов созданы',
                'creating_launchers': '🚀 Создание скриптов запуска...',
                'launchers_created': '✅ Скрипты запуска созданы',
                'setup_complete': '🎉 Настройка проекта завершена!',
                'next_steps': '📋 Что дальше:',
                'next_step1': '1. Запустите GUI: python gui_converter.py',
                'next_step2': '2. Или используйте CLI: python convert_media.py --help',
                'next_step3': '3. Если FFmpeg не найден, установите его или соберите из исходников',
                'setup_success': '✅ Проект успешно настроен!',
                'setup_error': '❌ Ошибка настройки проекта',
                'check_logs': 'Проверьте логи выше для получения дополнительной информации.',
                'windows_only': '❌ Этот скрипт предназначен только для Windows',
                'use_build_script': '💡 Для Linux/macOS используйте: python build_ffmpeg.py',
                'ffmpeg_installed': '🎉 Скачивание FFmpeg завершено успешно!',
                'ffmpeg_path': '📁 FFmpeg установлен в: {}',
                'use_wrapper': '🔧 Используйте ffmpeg.bat для запуска',
                'download_success': '✅ FFmpeg успешно скачан и установлен!',
                'download_error': '❌ Ошибка скачивания FFmpeg',
                'progress': '📊 Прогресс: {:.1f}%',
                'file': '📁 Файл: {}',
                'bin_folder_error': '❌ Папка bin не найдена в распакованном FFmpeg',
                'ffmpeg_exe_not_found': '❌ ffmpeg.exe не найден',
                'ffmpeg_run_error': '❌ Ошибка запуска FFmpeg: {}',
                'ffmpeg_folder_error': '❌ Не удалось найти папку с FFmpeg в архиве',
                'starting_setup': '🚀 Начинаем настройку проекта...',
                'starting_download': '🚀 Начинаем скачивание FFmpeg...',
                'system_check': '🔍 Проверка системы...',
                'system_windows': '✅ Система: Windows',
                'system_linux': '✅ Система: Linux',
                'system_macos': '✅ Система: macOS',
                'language_detected': '🌐 Определен язык: {}',
                'language_manual': '🌐 Используется язык: {}',
                'language_prompt': 'Выберите язык / Choose language (ru/en): ',
                'invalid_language': 'Неверный выбор. Используется русский. / Invalid choice. Using Russian.',
                'manual_language': 'Ручной выбор языка / Manual language selection',
                'auto_language': 'Автоматическое определение / Auto detection'
            },
            'en': {
                'title': '🎬 Media Converter Installer',
                'checking_python': '🐍 Checking Python version...',
                'python_version_error': '❌ Python 3.7 or higher required',
                'python_found': '✅ Python {} found',
                'installing_deps': '📦 Installing Python dependencies...',
                'deps_install_error': '❌ Error installing dependencies: {}',
                'deps_installed': '✅ Dependencies installed successfully',
                'ffmpeg_setup': '🎬 Setting up FFmpeg...',
                'ffmpeg_found_system': '✅ FFmpeg found in system',
                'ffmpeg_found_local': '✅ Local FFmpeg build found: {}',
                'ffmpeg_not_found': '⚠️ FFmpeg not found',
                'ffmpeg_options': 'Installation options:',
                'ffmpeg_option1': '1. Download from https://ffmpeg.org/ and add to PATH',
                'ffmpeg_option2': '2. Automatic installation (recommended)',
                'ffmpeg_option3': '3. Use your system package manager',
                'downloading_ffmpeg': '📥 Downloading FFmpeg...',
                'ffmpeg_download_error': '❌ Download error: {}',
                'ffmpeg_downloaded': '✅ Download completed',
                'extracting_ffmpeg': '📦 Extracting FFmpeg...',
                'ffmpeg_extract_error': '❌ Extraction error: {}',
                'ffmpeg_extracted': '✅ FFmpeg extracted to {}',
                'temp_file_deleted': '🗑️ Temporary file deleted',
                'creating_wrapper': '📝 Creating wrapper script...',
                'wrapper_created': '✅ Wrapper script created: {}',
                'testing_ffmpeg': '🧪 Testing FFmpeg...',
                'ffmpeg_test_error': '❌ Testing error: {}',
                'ffmpeg_works': '✅ FFmpeg works correctly',
                'creating_samples': '📝 Creating sample files...',
                'samples_created': '✅ Sample files created',
                'creating_launchers': '🚀 Creating launcher scripts...',
                'launchers_created': '✅ Launcher scripts created',
                'setup_complete': '🎉 Project setup completed!',
                'next_steps': '📋 What\'s next:',
                'next_step1': '1. Run GUI: python gui_converter.py',
                'next_step2': '2. Or use CLI: python convert_media.py --help',
                'next_step3': '3. If FFmpeg not found, install it or build from source',
                'setup_success': '✅ Project successfully configured!',
                'setup_error': '❌ Project setup error',
                'check_logs': 'Check logs above for additional information.',
                'windows_only': '❌ This script is for Windows only',
                'use_build_script': '💡 For Linux/macOS use: python build_ffmpeg.py',
                'ffmpeg_installed': '🎉 FFmpeg download completed successfully!',
                'ffmpeg_path': '📁 FFmpeg installed in: {}',
                'use_wrapper': '🔧 Use ffmpeg.bat to run',
                'download_success': '✅ FFmpeg successfully downloaded and installed!',
                'download_error': '❌ FFmpeg download error',
                'progress': '📊 Progress: {:.1f}%',
                'file': '📁 File: {}',
                'bin_folder_error': '❌ Bin folder not found in extracted FFmpeg',
                'ffmpeg_exe_not_found': '❌ ffmpeg.exe not found',
                'ffmpeg_run_error': '❌ FFmpeg run error: {}',
                'ffmpeg_folder_error': '❌ Could not find FFmpeg folder in archive',
                'starting_setup': '🚀 Starting project setup...',
                'starting_download': '🚀 Starting FFmpeg download...',
                'system_check': '🔍 Checking system...',
                'system_windows': '✅ System: Windows',
                'system_linux': '✅ System: Linux',
                'system_macos': '✅ System: macOS',
                'language_detected': '🌐 Language detected: {}',
                'language_manual': '🌐 Language used: {}',
                'language_prompt': 'Choose language / Выберите язык (ru/en): ',
                'invalid_language': 'Invalid choice. Using English. / Неверный выбор. Используется английский.',
                'manual_language': 'Manual language selection / Ручной выбор языка',
                'auto_language': 'Auto detection / Автоматическое определение'
            }
        }
    
    def _detect_language(self):
        """Определение языка системы"""
        try:
            # Пробуем определить язык системы
            system_lang = locale.getlocale()[0]
            if system_lang and system_lang.startswith('ru'):
                return 'ru'
            else:
                return 'en'
        except:
            return 'en'
    
    def get(self, key, *args):
        """Получение перевода"""
        translation = self.translations.get(self.current_lang, self.translations['en']).get(key, key)
        if args:
            return translation.format(*args)
        return translation
    
    def set_language(self, lang):
        """Установка языка"""
        if lang in self.translations:
            self.current_lang = lang
            return True
        return False
    
    def prompt_language(self):
        """Запрос языка у пользователя"""
        print(f"\n{self.get('manual_language')}")
        choice = input(self.get('language_prompt')).strip().lower()
        
        if choice in ['ru', 'рус', 'russian']:
            self.set_language('ru')
            print(f"{self.get('language_manual', 'Russian')}")
        elif choice in ['en', 'eng', 'english']:
            self.set_language('en')
            print(f"{self.get('language_manual', 'English')}")
        else:
            print(self.get('invalid_language'))
            self.set_language('ru' if self._detect_language() == 'ru' else 'en')

class UniversalInstaller:
    """Универсальный установщик"""
    
    def __init__(self):
        self.project_dir = Path.cwd()
        self.system = platform.system().lower()
        self.loc = Localization()
        
        # Определяем язык
        if len(sys.argv) > 1 and sys.argv[1] in ['--lang', '-l']:
            if len(sys.argv) > 2:
                self.loc.set_language(sys.argv[2])
            else:
                self.loc.prompt_language()
        else:
            print(f"{self.loc.get('language_detected', self.loc.get('auto_language'))}")
        
        print(f"\n{self.loc.get('title')}")
        print("=" * 50)
    
    def check_python_version(self) -> bool:
        """Проверка версии Python"""
        logger.info(self.loc.get('checking_python'))
        
        if sys.version_info < (3, 7):
            logger.error(self.loc.get('python_version_error'))
            return False
        
        logger.info(self.loc.get('python_found', sys.version.split()[0]))
        return True
    
    def install_dependencies(self) -> bool:
        """Установка Python зависимостей"""
        logger.info(self.loc.get('installing_deps'))
        
        try:
            # Обновляем pip
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         capture_output=True, check=True)
            
            # Устанавливаем зависимости
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         capture_output=True, check=True)
            
            logger.info(self.loc.get('deps_installed'))
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(self.loc.get('deps_install_error', str(e)))
            return False
    
    def check_ffmpeg(self) -> bool:
        """Проверка наличия FFmpeg"""
        logger.info(self.loc.get('ffmpeg_setup'))
        
        # Проверяем наличие FFmpeg в системе
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(self.loc.get('ffmpeg_found_system'))
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
                logger.info(self.loc.get('ffmpeg_found_local', path))
                return True
        
        return False
    
    def download_ffmpeg(self) -> bool:
        """Скачивание FFmpeg для Windows"""
        if self.system != "windows":
            logger.info(self.loc.get('use_build_script'))
            return False
        
        try:
            logger.info(self.loc.get('downloading_ffmpeg'))
            
            # URL для скачивания
            base_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest"
            arch = "win64" if platform.machine().endswith('64') else "win32"
            filename = f"ffmpeg-master-latest-{arch}-gpl.zip"
            url = f"{base_url}/{filename}"
            
            logger.info(self.loc.get('file', filename))
            
            # Скачиваем файл
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            logger.info(self.loc.get('progress', progress))
            
            logger.info(self.loc.get('ffmpeg_downloaded'))
            return self.extract_ffmpeg(filename)
            
        except Exception as e:
            logger.error(self.loc.get('ffmpeg_download_error', str(e)))
            return False
    
    def extract_ffmpeg(self, zip_filename: str) -> bool:
        """Распаковка FFmpeg"""
        try:
            logger.info(self.loc.get('extracting_ffmpeg'))
            
            bin_dir = Path("bin")
            bin_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(bin_dir)
            
            # Находим папку с FFmpeg
            ffmpeg_folders = list(bin_dir.glob("ffmpeg-*"))
            if ffmpeg_folders:
                ffmpeg_folder = ffmpeg_folders[0]
                ffmpeg_dir = bin_dir / "ffmpeg"
                ffmpeg_folder.rename(ffmpeg_dir)
                logger.info(self.loc.get('ffmpeg_extracted', ffmpeg_dir))
            else:
                logger.error(self.loc.get('ffmpeg_folder_error'))
                return False
            
            # Удаляем zip файл
            Path(zip_filename).unlink()
            logger.info(self.loc.get('temp_file_deleted'))
            
            return self.create_wrapper_script(ffmpeg_dir)
            
        except Exception as e:
            logger.error(self.loc.get('ffmpeg_extract_error', str(e)))
            return False
    
    def create_wrapper_script(self, ffmpeg_dir: Path) -> bool:
        """Создание скрипта-обертки"""
        logger.info(self.loc.get('creating_wrapper'))
        
        bin_path = ffmpeg_dir / "bin"
        if not bin_path.exists():
            logger.error(self.loc.get('bin_folder_error'))
            return False
        
        wrapper_content = f"""@echo off
set FFMPEG_PATH=%~dp0{ffmpeg_dir}\\bin
set PATH=%FFMPEG_PATH%;%PATH%
ffmpeg.exe %*
"""
        
        wrapper_path = Path("ffmpeg.bat")
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_content)
        
        logger.info(self.loc.get('wrapper_created', wrapper_path))
        return self.test_ffmpeg(ffmpeg_dir)
    
    def test_ffmpeg(self, ffmpeg_dir: Path) -> bool:
        """Тестирование FFmpeg"""
        try:
            logger.info(self.loc.get('testing_ffmpeg'))
            
            ffmpeg_exe = ffmpeg_dir / "bin" / "ffmpeg.exe"
            if not ffmpeg_exe.exists():
                logger.error(self.loc.get('ffmpeg_exe_not_found'))
                return False
            
            result = subprocess.run([str(ffmpeg_exe), "-version"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(self.loc.get('ffmpeg_works'))
                return True
            else:
                logger.error(self.loc.get('ffmpeg_run_error', result.stderr))
                return False
                
        except Exception as e:
            logger.error(self.loc.get('ffmpeg_test_error', str(e)))
            return False
    
    def create_sample_files(self):
        """Создание примеров файлов"""
        logger.info(self.loc.get('creating_samples'))
        
        examples_dir = Path("examples")
        examples_dir.mkdir(exist_ok=True)
        
        # Создаем README для примеров
        examples_readme = """# Примеры использования конвертера / Usage Examples

## Запуск GUI конвертера / Run GUI converter
```bash
python gui_converter.py
```

## Запуск командной строки конвертера / Run CLI converter
```bash
python convert_media.py "папка_с_файлами" -o "папка_для_сохранения" -q 80
```

## Сборка FFmpeg из исходников / Build FFmpeg from source
```bash
python build_ffmpeg.py
```

## Поддерживаемые форматы / Supported formats

### Видео / Video
- Входные / Input: MP4, AVI, MOV, MKV, WMV, FLV, WebM
- Выходные / Output: MP4, WebM, AVI, MKV, MOV

### Аудио / Audio
- Входные / Input: MP3, WAV, AAC, OGG, FLAC, M4A
- Выходные / Output: MP3, WAV, AAC, OGG, OPUS

### Изображения / Images
- Входные / Input: JPG, PNG, BMP, TIFF, WebP
- Выходные / Output: WebP, JPG, PNG
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
        
        logger.info(self.loc.get('samples_created'))
    
    def create_launcher_scripts(self):
        """Создание скриптов запуска"""
        logger.info(self.loc.get('creating_launchers'))
        
        if self.system == "windows":
            launchers = {
                "run_gui.bat": "@echo off\npython gui_converter.py\npause",
                "run_cli.bat": "@echo off\npython convert_media.py %*\npause",
                "build_ffmpeg.bat": "@echo off\npython build_ffmpeg.py\npause"
            }
        else:
            launchers = {
                "run_gui.sh": "#!/bin/bash\npython3 gui_converter.py",
                "run_cli.sh": "#!/bin/bash\npython3 convert_media.py \"$@\"",
                "build_ffmpeg.sh": "#!/bin/bash\npython3 build_ffmpeg.py"
            }
        
        for filename, content in launchers.items():
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            if not self.system == "windows":
                Path(filename).chmod(0o755)
        
        logger.info(self.loc.get('launchers_created'))
    
    def setup(self) -> bool:
        """Полная настройка проекта"""
        logger.info(self.loc.get('starting_setup'))
        
        # Проверяем систему
        logger.info(self.loc.get('system_check'))
        if self.system == "windows":
            logger.info(self.loc.get('system_windows'))
        elif self.system == "linux":
            logger.info(self.loc.get('system_linux'))
        elif self.system == "darwin":
            logger.info(self.loc.get('system_macos'))
        
        # Проверяем Python
        if not self.check_python_version():
            return False
        
        # Устанавливаем зависимости
        if not self.install_dependencies():
            return False
        
        # Настраиваем FFmpeg
        if not self.check_ffmpeg():
            logger.warning(self.loc.get('ffmpeg_not_found'))
            logger.info(self.loc.get('ffmpeg_options'))
            logger.info(self.loc.get('ffmpeg_option1'))
            logger.info(self.loc.get('ffmpeg_option2'))
            logger.info(self.loc.get('ffmpeg_option3'))
            
            # Пытаемся скачать FFmpeg для Windows
            if self.system == "windows":
                if self.download_ffmpeg():
                    logger.info(self.loc.get('ffmpeg_installed'))
                    logger.info(self.loc.get('ffmpeg_path', "bin/ffmpeg"))
                    logger.info(self.loc.get('use_wrapper'))
        
        # Создаем примеры файлов
        self.create_sample_files()
        
        # Создаем скрипты запуска
        self.create_launcher_scripts()
        
        logger.info(self.loc.get('setup_complete'))
        logger.info(f"\n{self.loc.get('next_steps')}")
        logger.info(self.loc.get('next_step1'))
        logger.info(self.loc.get('next_step2'))
        logger.info(self.loc.get('next_step3'))
        
        return True

def main():
    """Главная функция"""
    installer = UniversalInstaller()
    
    if installer.setup():
        print(f"\n{installer.loc.get('setup_success')}")
        print(installer.loc.get('check_logs'))
    else:
        print(f"\n{installer.loc.get('setup_error')}")
        print(installer.loc.get('check_logs'))

if __name__ == '__main__':
    main() 