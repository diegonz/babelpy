from abc import ABC, abstractmethod


class TranslateBackendHelper(ABC):
    """TranslateBackendHelper: Abstract class representing translate backend"""

    @abstractmethod
    def _translation_available(self, source_lang, target_lang):
        """Abstract method for checking translation availability"""
        pass

    @abstractmethod
    def _translate(self, clipboard_content, translate_direction):
        """Abstract method for doing the real translation"""
        pass

    @abstractmethod
    def translate_auto(self, clipboard_content, target_lang):
        """Abstract method for requesting auto translation"""
        pass

    @abstractmethod
    def translate_manual(self, clipboard_content, source_lang, target_lang):
        """Abstract method for requesting manual translation"""
        pass
