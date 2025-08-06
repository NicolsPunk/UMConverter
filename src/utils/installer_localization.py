#!/usr/bin/env python3
"""
Модуль локализации для установщика
Localization module for installer
"""

import locale
import sys

class InstallerLocalization:
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
                'next_step1': '1. Запустите GUI: python src/gui/gui_converter.py',
                'next_step2': '2. Или используйте CLI: python src/cli/convert_media.py --help',
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
                'auto_language': 'Автоматическое определение / Auto detection',
                'unsupported_system': '❌ Неподдерживаемая система: {}',
                'linux_ffmpeg_help': '💡 Для Linux установите FFmpeg через пакетный менеджер: sudo apt install ffmpeg',
                'macos_ffmpeg_help': '💡 Для macOS установите FFmpeg через Homebrew: brew install ffmpeg',
                'creating_project_structure': '📁 Создание структуры проекта...',
                'project_structure_created': '✅ Структура проекта создана',
                'moving_files': '📦 Перемещение файлов...',
                'files_moved': '✅ Файлы перемещены',
                'creating_init_files': '📝 Создание __init__.py файлов...',
                'init_files_created': '✅ __init__.py файлы созданы'
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
                'next_step1': '1. Run GUI: python src/gui/gui_converter.py',
                'next_step2': '2. Or use CLI: python src/cli/convert_media.py --help',
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
                'auto_language': 'Auto detection / Автоматическое определение',
                'unsupported_system': '❌ Unsupported system: {}',
                'linux_ffmpeg_help': '💡 For Linux install FFmpeg via package manager: sudo apt install ffmpeg',
                'macos_ffmpeg_help': '💡 For macOS install FFmpeg via Homebrew: brew install ffmpeg',
                'creating_project_structure': '📁 Creating project structure...',
                'project_structure_created': '✅ Project structure created',
                'moving_files': '📦 Moving files...',
                'files_moved': '✅ Files moved',
                'creating_init_files': '📝 Creating __init__.py files...',
                'init_files_created': '✅ __init__.py files created'
            }
        }
    
    def _detect_language(self):
        """Определение языка системы"""
        try:
            # Пробуем определить язык системы
            system_lang = locale.getlocale()[0]
            if system_lang and system_lang.lower().startswith('ru'):
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