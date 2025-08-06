#!/usr/bin/env python3
"""
Унифицированная система локализации для GUI конвертера
Unified localization system for GUI converter
"""

import json
import locale
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

class GUILocalization:
    """Унифицированный класс для управления локализацией GUI"""
    
    def __init__(self, language: Optional[str] = None):
        self.translations = {}
        self.language = language or self._detect_language()
        self._load_translations()
    
    def _detect_language(self) -> str:
        """Автоматическое определение языка системы"""
        try:
            # Пробуем определить язык системы
            system_lang = locale.getlocale()[0]
            if system_lang and system_lang.lower().startswith('ru'):
                return 'ru'
            else:
                return 'en'
        except:
            return 'en'
    
    def _load_translations(self):
        """Загрузка переводов из файлов"""
        # Ищем файлы локализации в нескольких местах
        possible_paths = [
            Path("locales"),  # Корневая папка проекта
            Path(__file__).parent.parent.parent / "locales",  # Относительно utils
            Path(__file__).parent.parent / "gui" / "locales",  # Старое расположение
        ]
        
        locales_dir = None
        for path in possible_paths:
            if path.exists() and path.is_dir():
                locales_dir = path
                break
        
        if not locales_dir:
            print("Warning: Locales directory not found")
            return
        
        # Загружаем русский язык (основной)
        ru_file = locales_dir / "ru.json"
        if ru_file.exists():
            try:
                with open(ru_file, 'r', encoding='utf-8') as f:
                    self.translations['ru'] = json.load(f)
            except Exception as e:
                print(f"Error loading Russian translations: {e}")
        
        # Загружаем английский язык
        en_file = locales_dir / "en.json"
        if en_file.exists():
            try:
                with open(en_file, 'r', encoding='utf-8') as f:
                    self.translations['en'] = json.load(f)
            except Exception as e:
                print(f"Error loading English translations: {e}")
        
        # Если запрошенный язык не найден, используем русский
        if self.language not in self.translations:
            self.language = 'ru' if 'ru' in self.translations else 'en'
    
    def get(self, key: str, **kwargs) -> str:
        """
        Получение перевода по ключу
        
        Args:
            key: Ключ перевода (может содержать точки для вложенных ключей)
            **kwargs: Параметры для форматирования строки
        
        Returns:
            Переведенная строка
        """
        try:
            # Разбираем ключ по точкам для доступа к вложенным ключам
            keys = key.split('.')
            value = self.translations[self.language]
            
            for k in keys:
                value = value[k]
            
            # Если есть параметры для форматирования
            if kwargs:
                return value.format(**kwargs)
            else:
                return value
                
        except (KeyError, TypeError):
            # Если перевод не найден, возвращаем ключ
            return key
    
    def set_language(self, language: str) -> bool:
        """Установка языка"""
        if language in self.translations:
            self.language = language
            return True
        return False
    
    def get_available_languages(self) -> list:
        """Получение списка доступных языков"""
        return list(self.translations.keys())
    
    def get_current_language(self) -> str:
        """Получение текущего языка"""
        return self.language
    
    def prompt_language(self):
        """Запрос языка у пользователя"""
        print(f"\nManual language selection / Ручной выбор языка")
        choice = input("Choose language / Выберите язык (ru/en): ").strip().lower()
        
        if choice in ['ru', 'рус', 'russian']:
            self.set_language('ru')
            print(f"Language used: Russian / Используется язык: Русский")
        elif choice in ['en', 'eng', 'english']:
            self.set_language('en')
            print(f"Language used: English / Используется язык: Английский")
        else:
            print("Invalid choice. Using Russian. / Неверный выбор. Используется русский.")
            self.set_language('ru' if self._detect_language() == 'ru' else 'en') 