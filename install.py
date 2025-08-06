#!/usr/bin/env python3
"""
Главный установщик для конвертера медиафайлов
Main installer for media converter
"""

import sys
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.installer.universal_installer import main

if __name__ == '__main__':
    main() 