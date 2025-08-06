# 🎬 Ultimate Media Converter

Универсальный конвертер медиафайлов с графическим интерфейсом и командной строкой.

Universal media converter with GUI and CLI interfaces.

## 📁 Структура проекта / Project Structure

```
UMConverter/
├── src/
│   ├── core/           # Основная логика / Core logic
│   ├── gui/            # Графический интерфейс / GUI components
│   │   └── gui_converter.py
│   ├── cli/            # Командная строка / CLI components
│   │   └── convert_media.py
│   ├── utils/          # Утилиты / Utilities
│   │   └── localization.py
│   └── installer/      # Установщик / Installer
│       ├── universal_installer.py
│       └── ffmpeg_downloader.py
├── bin/                # FFmpeg и другие бинарные файлы / FFmpeg and other binaries
├── converted/          # Конвертированные файлы / Converted files
├── samples/            # Примеры файлов / Sample files
├── install.py          # Главный установщик / Main installer
├── requirements.txt    # Python зависимости / Python dependencies
└── README.md
```

## 🚀 Быстрый старт / Quick Start

### Установка / Installation

1. **Клонируйте репозиторий / Clone the repository:**
   ```bash
   git clone <repository-url>
   cd UMConverter
   ```

2. **Запустите установщик / Run the installer:**
   ```bash
   python install.py
   ```

   Или с выбором языка / Or with language selection:
   ```bash
   python install.py --lang ru
   python install.py --lang en
   ```

### Использование / Usage

#### Графический интерфейс / GUI
```bash
python src/gui/gui_converter.py
```

#### Командная строка / CLI
```bash
python src/cli/convert_media.py --help
```

## 🔧 Возможности / Features

### Поддерживаемые форматы / Supported Formats

**Входные форматы / Input formats:**
- Видео / Video: MP4, AVI, MKV, MOV, WMV, FLV, WebM
- Аудио / Audio: MP3, WAV, FLAC, AAC, OGG, WMA
- Изображения / Images: JPG, PNG, BMP, GIF, TIFF, WebP

**Выходные форматы / Output formats:**
- Видео / Video: MP4, AVI, MKV, MOV, WebM
- Аудио / Audio: MP3, WAV, FLAC, AAC, OGG
- Изображения / Images: JPG, PNG, WebP

### Функции / Features

- 🎨 **Графический интерфейс** / **GUI Interface**
  - Простой и интуитивный интерфейс / Simple and intuitive interface
  - Предварительный просмотр / Preview functionality
  - Пакетная обработка / Batch processing

- 💻 **Командная строка** / **CLI Interface**
  - Полный контроль над параметрами / Full control over parameters
  - Автоматизация / Automation support
  - Скрипты / Scripting capabilities

- 🌐 **Многоязычность** / **Multilingual**
  - Русский / Russian
  - Английский / English

- 🔧 **Автоматическая установка** / **Auto Installation**
  - FFmpeg для Windows, Linux, macOS / FFmpeg for Windows, Linux, macOS
  - Python зависимости / Python dependencies
  - Структура проекта / Project structure

## 📋 Требования / Requirements

- Python 3.7+
- FFmpeg (устанавливается автоматически / installed automatically)
- Зависимости из requirements.txt / Dependencies from requirements.txt

## 🛠️ Установка FFmpeg / FFmpeg Installation

### Автоматическая установка / Automatic Installation
Установщик автоматически скачает и настроит FFmpeg для вашей системы.

The installer will automatically download and configure FFmpeg for your system.

### Ручная установка / Manual Installation

**Windows:**
1. Скачайте с https://ffmpeg.org/
2. Добавьте в PATH

**Linux:**
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS/RHEL
```

**macOS:**
```bash
brew install ffmpeg
```

## 📖 Использование / Usage

### Графический интерфейс / GUI

1. Запустите GUI / Run GUI:
   ```bash
   python src/gui/gui_converter.py
   ```

2. Выберите файлы для конвертации / Select files to convert
3. Настройте параметры / Configure parameters
4. Нажмите "Конвертировать" / Click "Convert"

### Командная строка / CLI

**Базовое использование / Basic usage:**
```bash
python src/cli/convert_media.py input.mp4 output.mp4
```

**С параметрами / With parameters:**
```bash
python src/cli/convert_media.py input.mp4 output.mp4 --format mp4 --quality high
```

**Пакетная обработка / Batch processing:**
```bash
python src/cli/convert_media.py *.mp4 --output-dir converted/ --format avi
```

**Помощь / Help:**
```bash
python src/cli/convert_media.py --help
```

## 🔧 Параметры CLI / CLI Parameters

- `--format`: Выходной формат / Output format
- `--quality`: Качество (low, medium, high) / Quality (low, medium, high)
- `--resolution`: Разрешение видео / Video resolution
- `--bitrate`: Битрейт / Bitrate
- `--fps`: Частота кадров / Frame rate
- `--output-dir`: Папка для выходных файлов / Output directory
- `--preset`: Пресет кодирования / Encoding preset

## 🐛 Устранение неполадок / Troubleshooting

### FFmpeg не найден / FFmpeg not found
1. Запустите установщик / Run the installer:
   ```bash
   python install.py
   ```

2. Или установите вручную / Or install manually (см. выше / see above)

### Ошибки Python / Python errors
1. Обновите Python до версии 3.7+ / Update Python to 3.7+
2. Установите зависимости / Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Проблемы с кодировкой / Encoding issues
1. Убедитесь, что FFmpeg установлен / Make sure FFmpeg is installed
2. Проверьте поддерживаемые форматы / Check supported formats
3. Попробуйте другие параметры качества / Try different quality parameters

## 🤝 Вклад в проект / Contributing

1. Форкните репозиторий / Fork the repository
2. Создайте ветку для новой функции / Create a feature branch
3. Внесите изменения / Make changes
4. Создайте Pull Request / Create a Pull Request

## 📄 Лицензия / License

MIT License

## 👥 Авторы / Authors

Media Converter Team

## 📞 Поддержка / Support

Если у вас есть вопросы или проблемы, создайте Issue в репозитории.

If you have questions or issues, create an Issue in the repository. 
