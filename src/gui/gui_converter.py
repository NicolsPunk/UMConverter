#!/usr/bin/env python3
"""
Современный GUI конвертер медиафайлов с переключением экранов
Поддерживает конвертацию любых форматов в любые форматы через FFmpeg
"""

import os
import threading
import subprocess
import logging
from pathlib import Path
from typing import Dict, List

import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

# Импорт локализации
try:
    from ..utils.gui_localization import GUILocalization
except ImportError:
    # Если относительный импорт не работает, пробуем абсолютный
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        from utils.gui_localization import GUILocalization
    except ImportError:
        # Fallback к старой локализации
        try:
            from .localization import Localization as GUILocalization
        except ImportError:
            print("Warning: Localization not found")
            GUILocalization = None

import json
import time
import re

# drag&drop
try:
    from tkinterdnd2 import TkinterDnD, DND_ALL
except ImportError:
    print("⚠️ tkinterdnd2 не установлен. Drag&drop будет недоступен.")
    TkinterDnD = None
    DND_ALL = None

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gui_conversion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Настройка customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Создаем класс CTk с поддержкой drag&drop
if TkinterDnD:
    class CTk(ctk.CTk, TkinterDnD.DnDWrapper):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.TkdndVersion = TkinterDnD._require(self)
else:
    CTk = ctk.CTk

class FFmpegConverter:
    """Класс для работы с FFmpeg"""
    
    def __init__(self):
        self.supported_formats = self._get_supported_formats()
        self.ffmpeg_path = self._find_ffmpeg()
        
    def _find_ffmpeg(self) -> str:
        """Поиск FFmpeg в системе или локальной сборке"""
        # Сначала проверяем локальную сборку
        local_paths = [
            "bin/bin/ffmpeg.exe",  # Windows
            "bin/bin/ffmpeg",      # Linux/macOS
            "bin/ffmpeg/bin/ffmpeg.exe",  # Скачанная версия
            "ffmpeg.bat",          # Windows wrapper
            "ffmpeg.sh"            # Linux/macOS wrapper
        ]
        
        for path in local_paths:
            if Path(path).exists():
                return path
        
        # Если локальная версия не найдена, используем системную
        return "ffmpeg"
    
    def _get_supported_formats(self) -> Dict[str, List[str]]:
        """Получение поддерживаемых форматов через FFmpeg"""
        formats = {
            'video': ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'm4v', '3gp', 'ogv'],
            'audio': ['mp3', 'wav', 'aac', 'ogg', 'flac', 'm4a', 'wma', 'opus'],
            'image': ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp', 'gif', 'ico', 'svg']
        }
        return formats
    
    def check_ffmpeg(self) -> bool:
        """Проверка наличия FFmpeg"""
        try:
            if self.ffmpeg_path.endswith('.bat') or self.ffmpeg_path.endswith('.sh'):
                # Для скриптов-оберток
                result = subprocess.run([self.ffmpeg_path, '-version'], 
                                      capture_output=True, text=True)
            else:
                # Для прямого вызова
                result = subprocess.run([self.ffmpeg_path, '-version'], 
                                      capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def get_file_info(self, file_path: str) -> Dict:
        """Получение информации о файле через FFmpeg"""
        try:
            # Определяем путь к ffprobe
            ffprobe_path = self.ffmpeg_path.replace('ffmpeg', 'ffprobe')
            if not Path(ffprobe_path).exists():
                ffprobe_path = 'ffprobe'  # Используем системную версию
            
            cmd = [
                ffprobe_path, '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', str(file_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {}
        except Exception as e:
            logger.error(f"Ошибка получения информации о файле: {e}")
            return {}
    
    def convert_file(self, input_path: str, output_path: str, 
                    video_codec: str = None, audio_codec: str = None,
                    quality: int = 80, callback=None) -> bool:
        """
        Конвертация файла через FFmpeg
        
        Args:
            input_path: Путь к входному файлу
            output_path: Путь к выходному файлу
            video_codec: Видеокодек (если None - автоматический выбор)
            audio_codec: Аудиокодек (если None - автоматический выбор)
            quality: Качество (1-100)
            callback: Функция обратного вызова для прогресса
        """
        try:
            # Базовые параметры
            cmd = [self.ffmpeg_path, '-i', str(input_path)]
            
            # Определяем тип файла по расширению
            input_ext = Path(input_path).suffix.lower()
            output_ext = Path(output_path).suffix.lower()
            
            # Настройки для видео
            if input_ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']:
                if video_codec:
                    cmd.extend(['-c:v', video_codec])
                else:
                    # Автоматический выбор кодека
                    if output_ext == '.webm':
                        cmd.extend(['-c:v', 'libvpx-vp9'])
                    elif output_ext == '.mp4':
                        cmd.extend(['-c:v', 'libx264'])
                    elif output_ext == '.avi':
                        cmd.extend(['-c:v', 'libxvid'])
                
                if audio_codec:
                    cmd.extend(['-c:a', audio_codec])
                else:
                    if output_ext == '.webm':
                        cmd.extend(['-c:a', 'libopus'])
                    else:
                        cmd.extend(['-c:a', 'aac'])
                
                # Настройки качества
                if output_ext == '.webm':
                    cmd.extend(['-crf', '30'])
                else:
                    cmd.extend(['-crf', str(31 - int(quality * 0.31))])
            
            # Настройки для аудио
            elif input_ext in ['.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a']:
                if audio_codec:
                    cmd.extend(['-c:a', audio_codec])
                else:
                    if output_ext == '.mp3':
                        cmd.extend(['-c:a', 'libmp3lame'])
                    elif output_ext == '.aac':
                        cmd.extend(['-c:a', 'aac'])
                    elif output_ext == '.ogg':
                        cmd.extend(['-c:a', 'libvorbis'])
                    elif output_ext == '.opus':
                        cmd.extend(['-c:a', 'libopus'])
                
                # Настройки качества для аудио
                if output_ext == '.mp3':
                    cmd.extend(['-b:a', f'{quality * 3}k'])
                elif output_ext == '.aac':
                    cmd.extend(['-b:a', f'{quality * 2}k'])
            
            # Настройки для изображений
            elif input_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']:
                if output_ext == '.webp':
                    cmd.extend(['-quality', str(quality)])
                elif output_ext == '.jpg':
                    cmd.extend(['-q:v', str(31 - int(quality * 0.31))])
            
            # Выходной файл
            cmd.extend(['-y', str(output_path)])
            
            # Запуск конвертации
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Ожидание завершения
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                logger.info(f"✅ Успешно конвертирован: {input_path} -> {output_path}")
                return True
            else:
                logger.error(f"❌ Ошибка конвертации: {stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ошибка конвертации {input_path}: {str(e)}")
            return False

class ModernConverterGUI:
    """Современный GUI конвертер с переключением экранов"""
    
    def __init__(self, language: str = "ru"):
        self.root = CTk()
        
        # Инициализация локализации
        if GUILocalization:
            self.loc = GUILocalization(language)
        else:
            # Fallback если локализация не найдена
            self.loc = None
            
        title = self.loc.get("app_title") if self.loc else "🎬 UMConverter"
        self.root.title(title)
        self.root.geometry("700x650")
        self.root.resizable(True, True)
        
        # Инициализация конвертера
        self.converter = FFmpegConverter()
        self.selected_files = []
        self.output_directory = ""
        self.conversion_running = False
        
        # Словарь для хранения выбранных форматов файлов
        self.file_formats = {}
        
        # Переменная для отслеживания предыдущего экрана
        self.previous_screen = None
        
        # Создание интерфейса
        self._create_widgets()
        self._check_dependencies()
        
        # Показываем стартовый экран
        self.show_start_screen()
    
    def _get_text(self, key: str, default: str = None) -> str:
        """Безопасное получение текста с fallback"""
        if self.loc:
            return self.loc.get(key)
        return default or key
    
    def _create_widgets(self):
        """Создание виджетов интерфейса"""
        
        # Главный контейнер
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Создание фреймов для разных экранов
        self._create_start_frame()
        self._create_loading_frame()
        self._create_files_frame()
        self._create_output_frame()
        self._create_progress_frame()
        
        # Создание кнопок выбора языка и темы с абсолютной позицией
        self._create_language_button()
        self._create_theme_button()
    
    def _create_start_frame(self):
        """Создание стартового экрана с drag&drop"""
        
        self.start_frame = ctk.CTkFrame(self.main_frame)
        
        # Заголовок
        title_label = ctk.CTkLabel(
            self.start_frame, 
            text=self._get_text("main_title", "🎬 Ultimate Media Converter"),
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(50, 20))
        
        # Подзаголовок
        subtitle_label = ctk.CTkLabel(
            self.start_frame,
            text=self._get_text("subtitle"),
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 50))
        
        # Drag&drop область
        self.drop_area = ctk.CTkFrame(
            self.start_frame,
            fg_color=("gray85", "gray25"),
            corner_radius=15,
            border_width=3,
            border_color=("gray70", "gray30")
        )
        self.drop_area.pack(pady=(0, 50), padx=50, fill="both", expand=True)
        
        # Иконка и текст в drop области
        self.drop_content = ctk.CTkFrame(self.drop_area, fg_color="transparent")
        self.drop_content.pack(expand=True)
        
        self.drop_icon = ctk.CTkLabel(
            self.drop_content,
            text="📁",
            font=ctk.CTkFont(size=64)
        )
        self.drop_icon.pack(pady=(50, 20))
        
        self.drop_text = ctk.CTkLabel(
            self.drop_content,
            text=self._get_text("drop_area_text"),
            font=ctk.CTkFont(size=18),
            text_color="gray"
        )
        self.drop_text.pack(pady=(0, 50))
        
        # Привязка событий для hover эффектов
        self.drop_area.bind("<Button-1>", self._on_drop_area_click)
        self.drop_area.bind("<Enter>", self._on_drop_area_enter)
        self.drop_area.bind("<Leave>", self._on_drop_area_leave)
        
        # Привязка событий для дочерних элементов
        self.drop_content.bind("<Enter>", self._on_drop_area_enter)
        self.drop_content.bind("<Leave>", self._on_drop_area_leave)
        self.drop_icon.bind("<Enter>", self._on_drop_area_enter)
        self.drop_icon.bind("<Leave>", self._on_drop_area_leave)
        self.drop_text.bind("<Enter>", self._on_drop_area_enter)
        self.drop_text.bind("<Leave>", self._on_drop_area_leave)
        
        # Добавляем кнопку для выбора папки
        # folder_btn = ctk.CTkButton(
        #     self.start_frame,
        #     text="📁 Выбрать папку с файлами",
        #     command=self._select_folder_with_files,
        #     height=40,
        #     fg_color="gray"
        # )
        # folder_btn.pack(pady=(0, 20))
        
        # Настройка drag&drop для drop_area
        if TkinterDnD:
            self.drop_area.drop_target_register(DND_ALL)
            self.drop_area.dnd_bind("<<Drop>>", self._on_drop)
            self.drop_area.dnd_bind("<<DropEnter>>", self._on_drop_enter)
            self.drop_area.dnd_bind("<<DropLeave>>", self._on_drop_leave)
        
        # Статус FFmpeg
        self.ffmpeg_status_label = ctk.CTkLabel(
            self.start_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.ffmpeg_status_label.pack(pady=(40, 0))

    def _change_language(self, choice):
        """Изменение языка интерфейса"""
        if "Русский" in choice:
            if self.loc:
                self.loc.set_language("ru")
        elif "English" in choice:
            if self.loc:
                self.loc.set_language("en")
        
        # Обновляем все тексты интерфейса
        self._update_interface_texts()
    
    def _change_theme(self, choice):
        """Изменение темы"""
        if "Темная" in choice or "Dark" in choice:
            ctk.set_appearance_mode("dark")
        elif "Светлая" in choice or "Light" in choice:
            ctk.set_appearance_mode("light")
        elif "Системная" in choice or "System" in choice:
            ctk.set_appearance_mode("system")
    
    def _create_language_button(self):
        """Создание кнопки выбора языка"""
        self.language_button = ctk.CTkButton(
            self.root,
            text=("🌐" + self._get_text("language.title")),
            font=ctk.CTkFont(size=16, weight="bold"),
            width=80,
            height=35,
            command=self._show_language_menu,
            fg_color="gray",
            bg_color="transparent",
            hover_color="darkgray",
            corner_radius=10
        )
        
        self.language_button.place(relx=0.05, rely=0.05, anchor="nw")
        self.language_button.lift()
    
    def _create_theme_button(self):
        """Создание кнопки выбора темы"""
        self.theme_button = ctk.CTkButton(
            self.root,
            text=("🎨" + self._get_text("theme.title")),
            font=ctk.CTkFont(size=16, weight="bold"),
            width=80,
            height=35,
            command=self._show_theme_menu,
            fg_color="gray",
            bg_color="transparent",
            hover_color="darkgray",
            corner_radius=10
        )
        
        self.theme_button.place(relx=0.95, rely=0.05, anchor="ne")
        self.theme_button.lift()
    
    def _show_language_menu(self):
        """Показать меню выбора языка"""
        # Создаем всплывающее меню
        menu = tk.Menu(self.root, tearoff=0)
        
        # Добавляем опции языков
        menu.add_command(
            label=self._get_text("🇷🇺 Русский"),
            command=lambda: self._change_language("🇷🇺 Русский")
        )
        menu.add_command(
            label=self._get_text("🇺🇸 English"),
            command=lambda: self._change_language("🇺🇸 English")
        )
        
        # Показываем меню рядом с кнопкой
        x = self.language_button.winfo_rootx()
        y = self.language_button.winfo_rooty() + self.language_button.winfo_height()
        menu.post(x, y)
    
    def _show_theme_menu(self):
        """Показать меню выбора темы"""
        # Создаем всплывающее меню
        menu = tk.Menu(self.root, tearoff=0)
        
        # Добавляем опции тем
        menu.add_command(
            label=self._get_text("theme.dark", "🌙 Темная"),
            command=lambda: self._change_theme("🌙 Темная")
        )
        menu.add_command(
            label=self._get_text("theme.light", "☀️ Светлая"),
            command=lambda: self._change_theme("☀️ Светлая")
        )
        menu.add_command(
            label=self._get_text("theme.system", "🔄 Системная"),
            command=lambda: self._change_theme("🔄 Системная")
        )
        
        # Показываем меню рядом с кнопкой
        x = self.theme_button.winfo_rootx() - 100  # Смещаем влево
        y = self.theme_button.winfo_rooty() + self.theme_button.winfo_height()
        menu.post(x, y)
    
    def _create_loading_frame(self):
        """Создание экрана загрузки"""
        
        self.loading_frame = ctk.CTkFrame(self.main_frame)
        
        # Заголовок
        self.loading_title = ctk.CTkLabel(
            self.loading_frame,
            text=self._get_text("loading_title"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.loading_title.pack(pady=(100, 50))
        
        # Индикатор загрузки
        self.loading_progress = ctk.CTkProgressBar(
            self.loading_frame,
            mode="indeterminate",
            width=400,
            height=8
        )
        self.loading_progress.pack(pady=(0, 30))
        
        # Текст статуса
        self.loading_status = ctk.CTkLabel(
            self.loading_frame,
            text=self._get_text("loading_status"),
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.loading_status.pack()
    
    def _create_files_frame(self):
        """Создание экрана со списком файлов"""
        
        self.files_frame = ctk.CTkFrame(self.main_frame)
        
        # Заголовок
        self.files_title = ctk.CTkLabel(
            self.files_frame,
            text=self._get_text("files_title"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.files_title.pack(pady=(30, 20))
        
        # Scrollable frame для файлов
        self.files_scroll_frame = ctk.CTkScrollableFrame(
            self.files_frame,
            width=800,
            height=400
        )
        self.files_scroll_frame.pack(pady=(0, 30), padx=20)
        
        # Кнопки управления
        buttons_frame = ctk.CTkFrame(self.files_frame)
        buttons_frame.pack(pady=(0, 30))
        
        self.back_btn = ctk.CTkButton(
            buttons_frame,
            text=self._get_text("back_btn"),
            command=self.show_start_screen,
            height=40
        )
        self.back_btn.pack(side="left", padx=(0, 10))
        
        self.convert_btn = ctk.CTkButton(
            buttons_frame,
            text=self._get_text("convert_btn"),
            command=self.show_output_screen,
            height=40,
            fg_color="green"
        )
        self.convert_btn.pack(side="left")
    
    def _create_output_frame(self):
        """Создание экрана выбора выходной папки"""
        
        self.output_frame = ctk.CTkFrame(self.main_frame)
        
        # Заголовок
        self.output_title = ctk.CTkLabel(
            self.output_frame,
            text=self._get_text("output_title"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.output_title.pack(pady=(50, 30))
        
        # Текущая папка
        self.output_path_var = tk.StringVar(value="converted")
        self.output_path_label = ctk.CTkLabel(
            self.output_frame,
            textvariable=self.output_path_var,
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.output_path_label.pack(pady=(0, 20))
        
        # Кнопка выбора папки
        self.select_output_btn = ctk.CTkButton(
            self.output_frame,
            text=self._get_text("select_output_btn"),
            command=self._select_output_folder,
            height=40
        )
        self.select_output_btn.pack(pady=(0, 50))
        
        # Кнопки управления
        buttons_frame = ctk.CTkFrame(self.output_frame)
        buttons_frame.pack()
        
        self.output_back_btn = ctk.CTkButton(
            buttons_frame,
            text=self._get_text("back_btn"),
            command=self.show_files_screen,
            height=40
        )
        self.output_back_btn.pack(side="left", padx=(0, 10))
        
        self.start_convert_btn = ctk.CTkButton(
            buttons_frame,
            text=self._get_text("start_convert_btn"),
            command=self.start_conversion,
            height=40,
            fg_color="green"
        )
        self.start_convert_btn.pack(side="left")
    
    def _create_progress_frame(self):
        """Создание экрана прогресса"""
        
        self.progress_frame = ctk.CTkFrame(self.main_frame)
        
        # Заголовок
        self.progress_title = ctk.CTkLabel(
            self.progress_frame,
            text=self._get_text("progress_title"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.progress_title.pack(pady=(30, 20))
        
        # Прогресс бар
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=600,
            height=20
        )
        self.progress_bar.pack(pady=(0, 20))
        self.progress_bar.set(0)
        
        # Статус
        self.progress_status = ctk.CTkLabel(
            self.progress_frame,
            text=self._get_text("progress_status_ready"),
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.progress_status.pack(pady=(0, 20))
        
        # Лог конвертации
        self.log_text = ctk.CTkTextbox(
            self.progress_frame,
            width=800,
            height=300
        )
        self.log_text.pack(pady=(0, 30))
        
        # Кнопки управления
        buttons_frame = ctk.CTkFrame(self.progress_frame)
        buttons_frame.pack(pady=(20, 0))
        
        # Кнопка остановки
        self.stop_btn = ctk.CTkButton(
            buttons_frame,
            text=self._get_text("stop_btn"),
            command=self._stop_conversion,
            height=40,
            fg_color="orange"
        )
        self.stop_btn.pack(side="left")
    
    def _check_dependencies(self):
        """Проверка зависимостей"""
        if self.converter.check_ffmpeg():
            self.ffmpeg_status_label.configure(
                text=self._get_text("ffmpeg_status_ok"),
                text_color="green"
            )
        else:
            self.ffmpeg_status_label.configure(
                text=self._get_text("ffmpeg_status_error"),
                text_color="red"
            )
    

    
    def _update_interface_texts(self):
        """Обновление всех текстов интерфейса при смене языка"""
        # Обновляем заголовки и кнопки
        if hasattr(self, 'drop_text'):
            self.drop_text.configure(text=self.loc.get("drop_area_text"))
        
        if hasattr(self, 'back_btn'):
            self.back_btn.configure(text=self.loc.get("back_btn"))
        
        if hasattr(self, 'convert_btn'):
            self.convert_btn.configure(text=self.loc.get("convert_btn"))
        
        if hasattr(self, 'select_output_btn'):
            self.select_output_btn.configure(text=self.loc.get("select_output_btn"))
        
        if hasattr(self, 'start_convert_btn'):
            self.start_convert_btn.configure(text=self.loc.get("start_convert_btn"))
        
        if hasattr(self, 'stop_btn'):
            self.stop_btn.configure(text=self.loc.get("stop_btn"))
        
        if hasattr(self, 'progress_status'):
            self.progress_status.configure(text=self.loc.get("progress_status_ready"))
        
        # Обновляем кнопки языка и темы
        if hasattr(self, 'language_button'):
            self.language_button.configure(text=self._get_text("language.title", "🌐"))
        
        if hasattr(self, 'theme_button'):
            self.theme_button.configure(text=self._get_text("theme.title", "🎨"))
        
        # Обновляем заголовки экранов
        if hasattr(self, 'files_title'):
            self.files_title.configure(text=self._get_text("files_title"))
        
        if hasattr(self, 'output_title'):
            self.output_title.configure(text=self._get_text("output_title"))
        
        if hasattr(self, 'progress_title'):
            self.progress_title.configure(text=self._get_text("progress_title"))
        
        if hasattr(self, 'loading_title'):
            self.loading_title.configure(text=self._get_text("loading_title"))
        
        # Обновляем статус FFmpeg
        if hasattr(self, 'ffmpeg_status_label'):
            if self.converter.check_ffmpeg():
                self.ffmpeg_status_label.configure(
                    text=self.loc.get("ffmpeg_status_ok"),
                    text_color="green"
                )
            else:
                self.ffmpeg_status_label.configure(
                    text=self.loc.get("ffmpeg_status_error"),
                    text_color="red"
                )
    
    def _on_drop_area_click(self, event):
        """Обработка клика по области drag&drop"""
        self._select_files()
    
    def _on_drop_area_enter(self, event):
        """Обработка входа в область drag&drop"""
        self.drop_area.configure(
            fg_color=("gray75", "gray35"),
            border_color=("gray60", "gray40")
        )
        self.drop_text.configure(text=self._get_text("drop_area_hover"))
    
    def _on_drop_area_leave(self, event):
        """Обработка выхода из области drag&drop"""
        self.drop_area.configure(
            fg_color=("gray85", "gray25"),
            border_color=("gray70", "gray30")
        )
        self.drop_text.configure(text=self._get_text("drop_area_text"))
    
    def _on_drop_enter(self, event):
        """Обработка входа в область drag&drop с файлами"""
        self.drop_area.configure(
            fg_color=("gray75", "gray35"),
            border_color=("gray60", "gray40")
        )
        self.drop_text.configure(text=self._get_text("drop_area_hover"))
    
    def _on_drop_leave(self, event):
        """Обработка выхода из области drag&drop с файлами"""
        self.drop_area.configure(
            fg_color=("gray85", "gray25"),
            border_color=("gray70", "gray30")
        )
        self.drop_text.configure(text=self._get_text("drop_area_text"))
    
    def _on_drop(self, event):
        """Обработка сброса файлов"""
        try:
            # Получаем данные о сброшенных файлах
            dropped_data = event.data
            logger.info(f"Получены данные drag&drop: {dropped_data}")
            
            # Очищаем данные от фигурных скобок
            if dropped_data.startswith("{") and dropped_data.endswith("}"):
                dropped_data = dropped_data[1:-1]
            
            # Разбираем файлы
            files = []
            
            # Определяем ОС
            import platform
            system = platform.system().lower()
            
            if system == "windows":
                # Для Windows: ищем пути вида C:/path/to/file.ext
                pattern = r'[A-Za-z]:/[^{}]*?\.\w+(?:\s|$)'
            elif system == "darwin":  # macOS
                # Для macOS: ищем пути вида /path/to/file.ext
                pattern = r'/[^{}]*?\.\w+(?:\s|$)'
            else:  # Linux
                # Для Linux: ищем пути вида /path/to/file.ext
                pattern = r'/[^{}]*?\.\w+(?:\s|$)'


            logger.info("Пробуем finditer для поиска полных путей...")
            matches = re.finditer(pattern, dropped_data, re.IGNORECASE)
            
            # Список поддерживаемых расширений
            supported_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', 
                                   '.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a', 
                                   '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
            
            for match in matches:
                full_path = match.group(0).strip()  # Полный путь
                
                # Проверяем расширение файла
                file_ext = os.path.splitext(full_path)[1].lower()
                if file_ext not in supported_extensions:
                    logger.info(f"Пропускаем файл с неподдерживаемым расширением: {full_path}")
                    continue
                
                if full_path and os.path.exists(full_path):
                    files.append(full_path)
                    logger.info(f"Добавлен файл (finditer): {full_path}")
                else:
                    logger.warning(f"Файл не найден (finditer): {full_path}")
            
            if files:
                logger.info(f"Всего найдено файлов: {len(files)}")
                self.selected_files = files
                self.show_loading_screen()
            else:
                logger.error("Не удалось найти ни одного файла")
                CTkMessagebox(
                    title="Предупреждение",
                    message=self._get_text("messages.no_files_found"),
                    icon="warning"
                )
                
        except Exception as e:
            logger.error(f"Ошибка обработки drag&drop: {e}")
            CTkMessagebox(
                title="Ошибка",
                message=self._get_text("messages.drop_error", error=str(e)),
                icon="cancel"
            )
    
    def _select_files(self):
        """Выбор файлов"""
        files = filedialog.askopenfilenames(
            title="Выберите файлы для конвертации",
            filetypes=[
                ("Все медиафайлы", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.mp3 *.wav *.aac *.ogg *.flac *.m4a *.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
                ("Видео файлы", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
                ("Аудио файлы", "*.mp3 *.wav *.aac *.ogg *.flac *.m4a"),
                ("Изображения", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
                ("Все файлы", "*.*")
            ]
        )
        
        if files:
            self.selected_files = list(files)
            self.show_loading_screen()
    
    def _select_folder_with_files(self):
        """Выбор папки с автоматическим поиском медиафайлов"""
        folder = filedialog.askdirectory(title="Выберите папку с медиафайлами")
        
        if folder:
            # Поиск всех медиафайлов в папке
            media_extensions = [
                '*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv', '*.webm',
                '*.mp3', '*.wav', '*.aac', '*.ogg', '*.flac', '*.m4a',
                '*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp'
            ]
            
            files = []
            for ext in media_extensions:
                files.extend(Path(folder).glob(ext))
                files.extend(Path(folder).glob(ext.upper()))
            
            if files:
                self.selected_files = [str(f) for f in files]
                logger.info(f"Найдено {len(self.selected_files)} файлов в папке {folder}")
                self.show_loading_screen()
            else:
                CTkMessagebox(
                    title="Предупреждение",
                    message=self._get_text("messages.no_media_files"),
                    icon="warning"
                )
    
    def show_start_screen(self):
        """Показать стартовый экран"""
        self._hide_all_frames()
        self.start_frame.pack(fill="both", expand=True)
    
    def show_loading_screen(self):
        """Показать экран загрузки"""
        self._hide_all_frames()
        self.loading_frame.pack(fill="both", expand=True)
        
        # Запускаем анимацию загрузки
        self.loading_progress.start()
        
        # Запускаем анализ файлов в отдельном потоке
        thread = threading.Thread(target=self._analyze_files)
        thread.daemon = True
        thread.start()
    
    def show_files_screen(self):
        """Показать экран со списком файлов"""
        self._hide_all_frames()
        self.files_frame.pack(fill="both", expand=True)
        self._populate_files_list()
    
    def show_output_screen(self):
        """Показать экран выбора выходной папки"""
        self._hide_all_frames()
        self.output_frame.pack(fill="both", expand=True)
        
        # Устанавливаем дефолтную папку
        default_output = Path.cwd() / "converted"
        self.output_directory = str(default_output)
        self.output_path_var.set(str(default_output))
    
    def show_progress_screen(self):
        """Показать экран прогресса"""
        self._hide_all_frames()
        self.progress_frame.pack(fill="both", expand=True)
    
    def _hide_all_frames(self):
        """Скрыть все фреймы"""
        for frame in [self.start_frame, self.loading_frame, self.files_frame, 
                     self.output_frame, self.progress_frame]:
            frame.pack_forget()
    
    def _analyze_files(self):
        """Анализ файлов в отдельном потоке"""
        try:
            # Имитируем анализ файлов
            for i, file_path in enumerate(self.selected_files):
                self.loading_status.configure(text=f"Анализ файла {i+1}/{len(self.selected_files)}...")
                time.sleep(0.5)  # Имитация работы
            
            # Переходим к экрану файлов
            self.root.after(0, self.show_files_screen)
            
        except Exception as e:
            logger.error(f"Ошибка анализа файлов: {e}")
            self.root.after(0, self.show_start_screen)
    
    def _populate_files_list(self):
        """Заполнение списка файлов"""
        # Очищаем старые виджеты
        for widget in self.files_scroll_frame.winfo_children():
            widget.destroy()
        
        # Добавляем файлы
        for i, file_path in enumerate(self.selected_files):
            self._create_file_item(file_path, i)
    
    def _create_file_item(self, file_path: str, index: int):
        """Создание элемента файла в списке"""
        file_frame = ctk.CTkFrame(self.files_scroll_frame)
        file_frame.pack(fill="x", pady=5, padx=10)
        
        # Иконка файла
        icon_frame = ctk.CTkFrame(file_frame, fg_color="transparent", width=50)
        icon_frame.pack(side="left", padx=(10, 5), pady=10)
        icon_frame.pack_propagate(False)
        
        # Определяем иконку по типу файла
        current_ext = Path(file_path).suffix.lower()
        file_type = self._get_file_type(current_ext)
        
        if file_type == "video":
            icon_text = "🎬"
        elif file_type == "audio":
            icon_text = "🎵"
        elif file_type == "image":
            icon_text = "🖼️"
        else:
            icon_text = "📄"
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text=icon_text,
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(expand=True)
        
        # Информация о файле
        file_info = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_info.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        
        # Имя файла
        file_name = Path(file_path).name
        name_label = ctk.CTkLabel(
            file_info,
            text=file_name,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.pack(anchor="w")
        
        # Текущий формат
        format_label = ctk.CTkLabel(
            file_info,
            text=self._get_text("current_format"),
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        format_label.pack(anchor="w")
        
        # Выбор выходного формата
        format_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        format_frame.pack(side="right", padx=10, pady=10)
        
        # Определяем доступные форматы из локализации
        formats = self._get_text("formats." + file_type)
        if not formats:
            # Fallback форматы
            if file_type == "video":
                formats = ["mp4", "webm", "avi", "mkv", "mov"]
            elif file_type == "audio":
                formats = ["mp3", "wav", "aac", "ogg", "opus"]
            elif file_type == "image":
                formats = ["webp", "jpg", "png"]
            else:
                formats = ["mp4", "webm", "avi", "mkv", "mov", "mp3", "wav", "aac", "ogg", "opus", "webp", "jpg", "png"]
        
        format_combo = ctk.CTkComboBox(
            format_frame,
            values=formats,
            width=100
        )
        
        # Устанавливаем значение из сохраненного выбора или первое доступное
        if index in self.file_formats:
            saved_format = self.file_formats[index].get()
            if saved_format in formats:
                format_combo.set(saved_format)
            else:
                format_combo.set(formats[0])
        else:
            format_combo.set(formats[0])
        
        format_combo.pack(side="left", padx=(0, 10))
        
        # Сохраняем ссылку на combo box для получения выбранного формата
        self.file_formats[index] = format_combo
        
        # Кнопка удаления
        delete_btn = ctk.CTkButton(
            format_frame,
            text=self._get_text("delete_btn"),
            width=30,
            height=30,
            command=lambda idx=index: self._remove_file(idx)
        )
        delete_btn.pack(side="left")
    
    def _get_file_type(self, extension: str) -> str:
        """Определение типа файла по расширению"""
        video_exts = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
        audio_exts = ['.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a']
        image_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        
        if extension in video_exts:
            return "video"
        elif extension in audio_exts:
            return "audio"
        elif extension in image_exts:
            return "image"
        else:
            return "unknown"
    
    def _remove_file(self, index: int):
        """Удаление файла из списка"""
        if 0 <= index < len(self.selected_files):
            # Удаляем файл из списка
            self.selected_files.pop(index)
            
            # Обновляем индексы в словаре форматов
            new_file_formats = {}
            for old_index, combo in self.file_formats.items():
                if old_index < index:
                    # Индексы до удаляемого файла остаются без изменений
                    new_file_formats[old_index] = combo
                elif old_index > index:
                    # Индексы после удаляемого файла сдвигаются на 1
                    new_file_formats[old_index - 1] = combo
            
            self.file_formats = new_file_formats
            
            # Пересоздаем список файлов
            self._populate_files_list()
    
    def _select_output_folder(self):
        """Выбор выходной папки"""
        folder = filedialog.askdirectory(
            title="Выберите папку для сохранения",
            initialdir=self.output_directory
        )
        
        if folder:
            self.output_directory = folder
            self.output_path_var.set(folder)
    
    def start_conversion(self):
        """Начало конвертации"""
        if not self.selected_files:
            CTkMessagebox(
                title="Предупреждение",
                message=self._get_text("messages.no_files_to_convert"),
                icon="warning"
            )
            return
        
        if not self.converter.check_ffmpeg():
            CTkMessagebox(
                title="Ошибка",
                message=self._get_text("messages.ffmpeg_not_found"),
                icon="cancel"
            )
            return
        
        # Создаем выходную папку
        output_path = Path(self.output_directory)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Переходим к экрану прогресса
        self.show_progress_screen()
        
        # Запускаем конвертацию в отдельном потоке
        thread = threading.Thread(target=self._conversion_worker)
        thread.daemon = True
        thread.start()
    
    def _stop_conversion(self):
        """Остановка конвертации"""
        self.conversion_running = False
        self.stop_btn.configure(state="disabled")
        self._log_message(self._get_text("conversion_stopped"))
    
    def _conversion_worker(self):
        """Рабочий поток конвертации"""
        try:
            total_files = len(self.selected_files)
            successful = 0
            failed = 0
            
            self.conversion_running = True
            self._log_message(self._get_text("conversion_started"))
            self.progress_status.configure(text=self._get_text("progress_status_converting"))
            
            for i, input_file in enumerate(self.selected_files):
                if not self.conversion_running:
                    break
                
                # Обновление прогресса
                progress = (i + 1) / total_files
                self.progress_bar.set(progress)
                
                # Определение выходного файла
                input_path = Path(input_file)
                
                # Получаем выбранный пользователем формат
                if hasattr(self, 'file_formats') and i in self.file_formats:
                    output_format = self.file_formats[i].get()
                else:
                    # Определяем формат по типу файла
                    current_ext = input_path.suffix.lower()
                    file_type = self._get_file_type(current_ext)
                    if file_type == "video":
                        output_format = "webm"
                    elif file_type == "audio":
                        output_format = "mp3"
                    elif file_type == "image":
                        output_format = "webp"
                    else:
                        output_format = "mp4"
                
                output_path = Path(self.output_directory) / f"{input_path.stem}.{output_format}"
                
                self._log_message(self._get_text("converting_file") + f"{input_path.name} -> {output_path.name}")
                
                # Конвертация
                if self.converter.convert_file(str(input_path), str(output_path), quality=80):
                    successful += 1
                    self._log_message(self._get_text("conversion_success") + f"{input_path.name}")
                else:
                    failed += 1
                    self._log_message(self._get_text("conversion_error") + f"{input_path.name}")
            
            # Завершение
            self.progress_bar.set(1.0)
            self._log_message(self._get_text("conversion_completed"))
            self._log_message(self._get_text("conversion_successful") + f"{successful}")
            self._log_message(self._get_text("conversion_failed") + f"{failed}")
            
            if failed == 0:
                self.progress_status.configure(text=self._get_text("progress_status_success"))
            else:
                self.progress_status.configure(text=self._get_text("progress_status_errors"))
            
            # Показываем сообщение о завершении
            self.root.after(2000, self._show_completion_message)
            
        except Exception as e:
            self._log_message(self._get_text("critical_error"))
            self.progress_status.configure(text="❌ Ошибка конвертации")
        
        finally:
            self.conversion_running = False
    
    def _show_completion_message(self):
        """Показать сообщение о завершении"""
        CTkMessagebox(
            title="Конвертация завершена",
            message=self._get_text("messages.conversion_complete"),
            icon="check"
        )
        
        # Возвращаемся к стартовому экрану
        self.show_start_screen()
    
    def _log_message(self, message: str):
        """Добавление сообщения в лог"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.root.update()
    
    def run(self):
        """Запуск GUI"""
        self.root.mainloop()

def main():
    """Главная функция"""
    # Можно передать язык как аргумент командной строки
    import sys
    language = "ru"  # По умолчанию русский
    if len(sys.argv) > 1:
        language = sys.argv[1]
    
    app = ModernConverterGUI(language)
    app.run()

if __name__ == '__main__':
    main() 