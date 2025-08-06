#!/usr/bin/env python3
"""
Универсальный установщик для конвертера медиафайлов
Universal installer for media converter
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import logging
import json

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.localization import Localization
from installer.ffmpeg_downloader import FFmpegDownloader

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    
    def setup_project_structure(self) -> bool:
        """Настройка структуры проекта"""
        logger.info(self.loc.get('creating_project_structure'))
        
        try:
            # Создаем структуру папок
            folders = [
                "src/core",
                "src/gui", 
                "src/cli",
                "src/utils",
                "src/installer",
                "bin",
                "converted",
                "samples"
            ]
            
            for folder in folders:
                Path(folder).mkdir(parents=True, exist_ok=True)
            
            logger.info(self.loc.get('project_structure_created'))
            return True
            
        except Exception as e:
            logger.error(f"Error creating project structure: {e}")
            return False
    
    def move_files(self) -> bool:
        """Перемещение файлов в новую структуру"""
        logger.info(self.loc.get('moving_files'))
        
        try:
            # Перемещаем основные файлы
            file_moves = [
                ("gui_converter.py", "src/gui/gui_converter.py"),
                ("convert_media.py", "src/cli/convert_media.py"),
                ("requirements.txt", "requirements.txt"),  # Оставляем в корне
            ]
            
            for src, dst in file_moves:
                if Path(src).exists():
                    shutil.move(src, dst)
            
            logger.info(self.loc.get('files_moved'))
            return True
            
        except Exception as e:
            logger.error(f"Error moving files: {e}")
            return False
    
    def create_init_files(self) -> bool:
        """Создание __init__.py файлов"""
        logger.info(self.loc.get('creating_init_files'))
        
        try:
            init_files = [
                "src/__init__.py",
                "src/core/__init__.py",
                "src/gui/__init__.py",
                "src/cli/__init__.py",
                "src/utils/__init__.py",
                "src/installer/__init__.py"
            ]
            
            for init_file in init_files:
                Path(init_file).touch()
            
            logger.info(self.loc.get('init_files_created'))
            return True
            
        except Exception as e:
            logger.error(f"Error creating init files: {e}")
            return False
    
    def create_gitignore(self) -> bool:
        """Создание .gitignore"""
        logger.info(self.loc.get('creating_samples'))
        
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
__init__.py

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
bin/

# OS
.DS_Store
Thumbs.db

# Project specific
converted/
*.bat
*.sh
samples/
"""
        
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        
        logger.info(self.loc.get('samples_created'))
        return True
    
    def create_launcher_scripts(self) -> bool:
        """Создание скриптов запуска"""
        logger.info(self.loc.get('creating_launchers'))
        
        try:
            if self.system == "windows":
                launchers = {
                    "run_gui.bat": "@echo off\npython src\\gui\\gui_converter.py\npause",
                    "run_cli.bat": "@echo off\npython src\\cli\\convert_media.py %*\npause",
                }
            else:
                launchers = {
                    "run_gui.sh": "#!/bin/bash\npython3 src/gui/gui_converter.py",
                    "run_cli.sh": "#!/bin/bash\npython3 src/cli/convert_media.py \"$@\"",
                }
            
            for filename, content in launchers.items():
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                
                if self.system != "windows":
                    Path(filename).chmod(0o755)
            
            logger.info(self.loc.get('launchers_created'))
            return True
            
        except Exception as e:
            logger.error(f"Error creating launchers: {e}")
            return False
    
    def setup_ffmpeg(self) -> bool:
        """Настройка FFmpeg"""
        if self.check_ffmpeg():
            return True
        
        logger.warning(self.loc.get('ffmpeg_not_found'))
        logger.info(self.loc.get('ffmpeg_options'))
        logger.info(self.loc.get('ffmpeg_option1'))
        logger.info(self.loc.get('ffmpeg_option2'))
        logger.info(self.loc.get('ffmpeg_option3'))
        
        # Пытаемся скачать FFmpeg
        downloader = FFmpegDownloader(self.loc)
        return downloader.download()
    
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
        else:
            logger.error(self.loc.get('unsupported_system', self.system))
            return False
        
        # Проверяем Python
        if not self.check_python_version():
            return False
        
        # Настраиваем структуру проекта
        if not self.setup_project_structure():
            return False
        
        # Перемещаем файлы
        if not self.move_files():
            return False
        
        # Создаем __init__.py файлы
        if not self.create_init_files():
            return False
        
        # Устанавливаем зависимости
        if not self.install_dependencies():
            return False
        
        # Настраиваем FFmpeg
        if not self.setup_ffmpeg():
            if self.system == "linux":
                logger.info(self.loc.get('linux_ffmpeg_help'))
            elif self.system == "darwin":
                logger.info(self.loc.get('macos_ffmpeg_help'))
        
        # Создаем .gitignore
        self.create_gitignore()
        
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