# 🎬 Ultimate Media Converter

[English](#english) | [Русский](#russian)

---

# 🇷🇺

### 📋 Описание
Современный конвертер медиафайлов с минималистичным интерфейсом, поддерживающий конвертацию видео, аудио и изображений в различные форматы. Проект включает в себя локальную сборку FFmpeg и автоматическую настройку.

### ✨ Возможности
- 🎬 **Универсальная конвертация** - Поддержка всех популярных форматов видео, аудио и изображений
- 🖥️ **Современный GUI** - Красивый интерфейс с drag&drop и многоэкранным процессом
- 🔧 **Локальный FFmpeg** - Автоматическая установка и настройка FFmpeg
- 🚀 **Автоматическая сборка** - Скрипты для сборки FFmpeg из исходников
- 📦 **Пакетная обработка** - Конвертация множества файлов одновременно
- 🌐 **Полная локализация** - Поддержка русского и английского языков

### 🎯 Поддерживаемые форматы

#### Видео
- **Входные**: MP4, AVI, MOV, MKV, WMV, FLV, WebM
- **Выходные**: MP4, WebM, AVI, MKV, MOV

#### Аудио
- **Входные**: MP3, WAV, AAC, OGG, FLAC, M4A
- **Выходные**: MP3, WAV, AAC, OGG, OPUS

#### Изображения
- **Входные**: JPG, PNG, BMP, TIFF, WebP
- **Выходные**: WebP, JPG, PNG

### 🚀 Быстрая установка

#### Автоматическая установка (рекомендуется)
```bash
# Скачать проект
git clone https://github.com/your-username/media-converter.git
cd media-converter

# Запустить универсальный установщик
python installer.py

# Или с выбором языка
python installer.py --lang ru
python installer.py --lang en
```

#### Ручная установка
```bash
# 1. Установить Python зависимости
pip install -r requirements.txt

# 2. Установить FFmpeg
# Windows: python installer.py (автоматически скачает)
# Linux/macOS: sudo apt install ffmpeg или brew install ffmpeg
```

### 🖥️ GUI интерфейс (рекомендуется)
```bash
python gui_converter.py
```

**Возможности GUI:**
- 🎯 **Стартовый экран** - Красивая область drag&drop для файлов
- ⏳ **Экран загрузки** - Анализ файлов с анимированным индикатором
- 📋 **Список файлов** - Просмотр и настройка параметров конвертации
- 📁 **Выбор папки** - Настройка выходной директории
- 📊 **Прогресс** - Отслеживание процесса конвертации
- ✅ **Уведомления** - Информативные сообщения о завершении

### 🛠️ Структура проекта
```
media-converter/
├── installer.py          # Универсальный установщик
├── gui_converter.py     # GUI конвертер
├── convert_media.py     # CLI конвертер
├── requirements.txt     # Python зависимости
├── README.md           # Документация
├── bin/               # Локальная сборка FFmpeg
└── ffmpeg.bat         # Скрипт-обертка для Windows
```

### 🔧 Дополнительные возможности

#### Универсальная конвертация
Конвертер автоматически определяет тип файла и предлагает подходящие форматы для конвертации.

#### Автоматический выбор кодеков
FFmpeg автоматически выбирает оптимальные кодеки для каждого формата.

#### Drag&Drop поддержка
Полная поддержка перетаскивания файлов с визуальными эффектами.

### 🔧 FFmpeg как сабмодуль
```bash
# Инициализация сабмодуля
git submodule add https://github.com/FFmpeg/FFmpeg.git ffmpeg

# Обновление сабмодуля
git submodule update --init --recursive

# Локальная сборка
python build_ffmpeg.py
```

**Преимущества:**
- ✅ Полный контроль над версией FFmpeg
- ✅ Возможность кастомизации сборки
- ✅ Независимость от системных зависимостей

### 🎉 Итоги проекта
- ✅ Современный GUI с drag&drop
- ✅ Универсальная конвертация медиафайлов
- ✅ Автоматическая установка FFmpeg
- ✅ Полная локализация (RU/EN)
- ✅ Поддержка всех популярных форматов
- ✅ Пакетная обработка файлов
- ✅ Кроссплатформенность

---

# 🇺🇸 

### 📋 Description
Modern media converter with beautiful GUI interface, supporting video, audio and image conversion to various formats. The project includes local FFmpeg build and automatic setup.

### ✨ Features
- 🎬 **Universal Conversion** - Support for all popular video, audio and image formats
- 🖥️ **Modern GUI** - Beautiful interface with drag&drop and multi-screen process
- 🔧 **Local FFmpeg** - Automatic FFmpeg installation and setup
- 🚀 **Automatic Build** - Scripts for building FFmpeg from source
- 📦 **Batch Processing** - Convert multiple files simultaneously
- 🌐 **Full Localization** - Russian and English language support

### 🎯 Supported Formats

#### Video
- **Input**: MP4, AVI, MOV, MKV, WMV, FLV, WebM
- **Output**: MP4, WebM, AVI, MKV, MOV

#### Audio
- **Input**: MP3, WAV, AAC, OGG, FLAC, M4A
- **Output**: MP3, WAV, AAC, OGG, OPUS

#### Images
- **Input**: JPG, PNG, BMP, TIFF, WebP
- **Output**: WebP, JPG, PNG

### 🚀 Quick Installation

#### Automatic Installation (recommended)
```bash
# Download project
git clone https://github.com/your-username/media-converter.git
cd media-converter

# Run universal installer
python installer.py

# Or with language selection
python installer.py --lang en
python installer.py --lang ru
```

#### Manual Installation
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install FFmpeg
# Windows: python installer.py (automatically downloads)
# Linux/macOS: sudo apt install ffmpeg or brew install ffmpeg
```

### 🖥️ GUI Interface (recommended)
```bash
python gui_converter.py
```

**GUI Features:**
- 🎯 **Start Screen** - Beautiful drag&drop area for files
- ⏳ **Loading Screen** - File analysis with animated indicator
- 📋 **File List** - View and configure conversion parameters
- 📁 **Folder Selection** - Configure output directory
- 📊 **Progress** - Track conversion process
- ✅ **Notifications** - Informative completion messages

### 🛠️ Project Structure
```
media-converter/
├── installer.py          # Universal installer
├── gui_converter.py     # GUI converter
├── convert_media.py     # CLI converter
├── build_ffmpeg.py      # FFmpeg build from source
├── requirements.txt     # Python dependencies
├── README.md           # Documentation
├── examples/           # Usage examples
├── bin/               # Local FFmpeg build
└── ffmpeg.bat         # Windows wrapper script
```

### 🔧 Additional Features

#### Universal Conversion
The converter automatically detects file type and suggests suitable formats for conversion.

#### Automatic Codec Selection
FFmpeg automatically selects optimal codecs for each format.

#### Drag&Drop Support
Full drag&drop support with visual effects.

### 🔧 FFmpeg as Submodule
```bash
# Initialize submodule
git submodule add https://github.com/FFmpeg/FFmpeg.git ffmpeg

# Update submodule
git submodule update --init --recursive

# Local build
python build_ffmpeg.py
```

**Benefits:**
- ✅ Full control over FFmpeg version
- ✅ Ability to customize build
- ✅ Independence from system dependencies

### 🎉 Project Results
- ✅ Modern GUI with drag&drop
- ✅ Universal media file conversion
- ✅ Automatic FFmpeg installation
- ✅ Full localization (RU/EN)
- ✅ Support for all popular formats
- ✅ Batch file processing
- ✅ Cross-platform compatibility

---

## 📄 License
MIT License - see LICENSE file for details

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support
If you have any questions or issues, please open an issue on GitHub. 
