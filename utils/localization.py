import json
from pathlib import Path
from typing import Dict

class Localization:
    """Handle multi-language support"""
    
    def __init__(self, default_lang: str = 'fa'):
        self.default_lang = default_lang
        self.locales: Dict[str, dict] = {}
        self.load_locales()
    
    def load_locales(self):
        """Load all language files from locales directory"""
        locales_dir = Path(__file__).parent.parent / 'locales'
        
        for locale_file in locales_dir.glob('*.json'):
            lang_code = locale_file.stem
            with open(locale_file, 'r', encoding='utf-8') as f:
                self.locales[lang_code] = json.load(f)
    
    def get(self, key: str, lang: str = None, **kwargs) -> str:
        """
        Get translated string
        
        Args:
            key: Translation key
            lang: Language code (defaults to default_lang)
            **kwargs: Format arguments for string interpolation
        
        Returns:
            Translated and formatted string
        """
        if lang is None:
            lang = self.default_lang
        
        # Fallback to default language if requested language not found
        if lang not in self.locales:
            lang = self.default_lang
        
        # Get translation or return key if not found
        translation = self.locales.get(lang, {}).get(key, key)
        
        # Format string with provided arguments
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except KeyError:
                pass
        
        return translation
    
    def get_available_languages(self) -> list:
        """Get list of available language codes"""
        return list(self.locales.keys())


# Global instance
i18n = Localization()