#!/usr/bin/env python3
"""
Модуль для скачивания FFmpeg
FFmpeg downloader module
"""

import platform
import zipfile
import requests
import subprocess
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FFmpegDownloader:
    """Класс для скачивания FFmpeg"""
    
    def __init__(self, localization):
        self.system = platform.system().lower()
        self.loc = localization
        self.bin_dir = Path("bin")
        self.ffmpeg_dir = self.bin_dir / "ffmpeg"
        
    def get_ffmpeg_url(self) -> str:
        """Получение URL для скачивания FFmpeg"""
        # Используем официальные сборки от BtbN
        base_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest"
        
        if self.system == "windows":
            # Определяем архитектуру для Windows
            if platform.machine().endswith('64'):
                arch = "win64"
            else:
                arch = "win32"
            filename = f"ffmpeg-master-latest-{arch}-gpl.zip"
        elif self.system == "linux":
            # Для Linux используем статические сборки
            if platform.machine().endswith('64'):
                arch = "linux64"
            else:
                arch = "linux32"
            filename = f"ffmpeg-master-latest-{arch}-static.tar.xz"
        elif self.system == "darwin":  # macOS
            if platform.machine() == "arm64":
                arch = "macos64"
            else:
                arch = "macos64"
            filename = f"ffmpeg-master-latest-{arch}-gpl.zip"
        else:
            raise ValueError(f"Unsupported system: {self.system}")
        
        return f"{base_url}/{filename}"
    
    def download_ffmpeg(self) -> bool:
        """Скачивание FFmpeg"""
        try:
            url = self.get_ffmpeg_url()
            filename = url.split('/')[-1]
            download_path = Path(filename)
            
            logger.info(self.loc.get('downloading_ffmpeg'))
            logger.info(self.loc.get('file', filename))
            
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
                            logger.info(self.loc.get('progress', progress))
            
            logger.info(self.loc.get('ffmpeg_downloaded'))
            return self.extract_ffmpeg(download_path)
            
        except Exception as e:
            logger.error(self.loc.get('ffmpeg_download_error', str(e)))
            return False
    
    def extract_ffmpeg(self, archive_path: Path) -> bool:
        """Распаковка FFmpeg"""
        try:
            logger.info(self.loc.get('extracting_ffmpeg'))
            
            # Создаем папку bin если её нет
            self.bin_dir.mkdir(exist_ok=True)
            
            if archive_path.suffix == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(self.bin_dir)
            elif archive_path.suffix == '.tar.xz':
                import tarfile
                with tarfile.open(archive_path, 'r:xz') as tar_ref:
                    tar_ref.extractall(self.bin_dir)
            else:
                logger.error(f"Unsupported archive format: {archive_path.suffix}")
                return False
            
            # Находим папку с FFmpeg
            ffmpeg_folders = list(self.bin_dir.glob("ffmpeg-*"))
            if ffmpeg_folders:
                ffmpeg_folder = ffmpeg_folders[0]
                # Переименовываем в ffmpeg
                ffmpeg_folder.rename(self.ffmpeg_dir)
                logger.info(self.loc.get('ffmpeg_extracted', self.ffmpeg_dir))
            else:
                logger.error(self.loc.get('ffmpeg_folder_error'))
                return False
            
            # Удаляем архив
            archive_path.unlink()
            logger.info(self.loc.get('temp_file_deleted'))
            
            return self.create_wrapper_script()
            
        except Exception as e:
            logger.error(self.loc.get('ffmpeg_extract_error', str(e)))
            return False
    
    def create_wrapper_script(self) -> bool:
        """Создание скрипта-обертки"""
        logger.info(self.loc.get('creating_wrapper'))
        
        if self.system == "windows":
            return self._create_windows_wrapper()
        else:
            return self._create_unix_wrapper()
    
    def _create_windows_wrapper(self) -> bool:
        """Создание Windows wrapper"""
        bin_path = self.ffmpeg_dir / "bin"
        
        if not bin_path.exists():
            logger.error(self.loc.get('bin_folder_error'))
            return False
        
        wrapper_content = f"""@echo off
set FFMPEG_PATH=%~dp0{self.ffmpeg_dir}\\bin
set PATH=%FFMPEG_PATH%;%PATH%
ffmpeg.exe %*
"""
        
        wrapper_path = Path("ffmpeg.bat")
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_content)
        
        logger.info(self.loc.get('wrapper_created', wrapper_path))
        return self.test_ffmpeg()
    
    def _create_unix_wrapper(self) -> bool:
        """Создание Unix wrapper"""
        bin_path = self.ffmpeg_dir / "bin"
        
        if not bin_path.exists():
            logger.error(self.loc.get('bin_folder_error'))
            return False
        
        wrapper_content = f"""#!/bin/bash
export FFMPEG_PATH="$(dirname "$0")/{self.ffmpeg_dir}/bin"
export PATH="$FFMPEG_PATH:$PATH"
ffmpeg "$@"
"""
        
        wrapper_path = Path("ffmpeg.sh")
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_content)
        
        # Делаем исполняемым
        wrapper_path.chmod(0o755)
        
        logger.info(self.loc.get('wrapper_created', wrapper_path))
        return self.test_ffmpeg()
    
    def test_ffmpeg(self) -> bool:
        """Тестирование FFmpeg"""
        try:
            logger.info(self.loc.get('testing_ffmpeg'))
            
            if self.system == "windows":
                ffmpeg_exe = self.ffmpeg_dir / "bin" / "ffmpeg.exe"
            else:
                ffmpeg_exe = self.ffmpeg_dir / "bin" / "ffmpeg"
            
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
    
    def download(self) -> bool:
        """Полный процесс скачивания"""
        logger.info(self.loc.get('starting_download'))
        
        # Скачиваем FFmpeg
        if not self.download_ffmpeg():
            return False
        
        logger.info(self.loc.get('ffmpeg_installed'))
        logger.info(self.loc.get('ffmpeg_path', self.ffmpeg_dir))
        
        if self.system == "windows":
            logger.info(self.loc.get('use_wrapper'))
        else:
            logger.info("🔧 Use ffmpeg.sh to run")
        
        return True 