# 🚀 Краткая инструкция по использованию / Quick Usage Guide

## 🇷🇺 Русский

### Быстрый старт
```bash
# 1. Клонировать проект
git clone https://github.com/your-username/media-converter.git
cd media-converter

# 2. Запустить установщик
python installer.py

# 3. Запустить GUI
python gui_converter.py
```

### Параметры установщика
```bash
# Автоматическое определение языка
python installer.py

# Ручной выбор языка
python installer.py --lang ru
python installer.py --lang en

# Интерактивный выбор языка
python installer.py --lang
```

### Использование GUI
1. **Стартовый экран**: Перетащите файлы в область или нажмите для выбора
2. **Анализ файлов**: Дождитесь завершения анализа
3. **Список файлов**: Настройте формат вывода для каждого файла
4. **Выбор папки**: Укажите папку для сохранения
5. **Конвертация**: Следите за прогрессом
6. **Готово**: Получите уведомление о завершении

### Использование CLI
```bash
# Конвертировать папку с файлами
python convert_media.py "папка_с_файлами"

# Указать выходную папку
python convert_media.py "папка_с_файлами" -o "папка_для_сохранения"

# Установить качество
python convert_media.py "папка_с_файлами" -q 80
```

---

## 🇺🇸 English

### Quick Start
```bash
# 1. Clone project
git clone https://github.com/your-username/media-converter.git
cd media-converter

# 2. Run installer
python installer.py

# 3. Launch GUI
python gui_converter.py
```

### Installer Parameters
```bash
# Auto language detection
python installer.py

# Manual language selection
python installer.py --lang en
python installer.py --lang ru

# Interactive language selection
python installer.py --lang
```

### GUI Usage
1. **Start Screen**: Drag files to area or click to select
2. **File Analysis**: Wait for analysis to complete
3. **File List**: Configure output format for each file
4. **Folder Selection**: Specify output directory
5. **Conversion**: Monitor progress
6. **Complete**: Receive completion notification

### CLI Usage
```bash
# Convert folder with files
python convert_media.py "folder_with_files"

# Specify output folder
python convert_media.py "folder_with_files" -o "output_folder"

# Set quality
python convert_media.py "folder_with_files" -q 80
```

---

## 🔧 Troubleshooting / Решение проблем

### Common Issues / Частые проблемы

#### FFmpeg not found / FFmpeg не найден
```bash
# Windows - автоматическая установка
python installer.py

# Linux
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

#### Python dependencies / Python зависимости
```bash
pip install -r requirements.txt
```

#### Drag&Drop not working / Drag&Drop не работает
```bash
pip install tkinterdnd2
```

---

## 📞 Support / Поддержка

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: See README.md for detailed information
- **Examples**: Check examples/ folder for usage examples 