from translation.TranslateException import TranslateException
from translation.TranslateHelper import TranslateBackendHelper
from translation.yandex.yandex_translator import YandexTranslator


class YandexHelperException(TranslateException):
    """
    Default YandexHelper exception
    """
    error_codes = {
        405: "ERR_TRANSLATION_NOT_AVAILABLE",
        406: "ERR_SAME_LANGUAGE_SOURCE_AND_TARGET",
        505: "ERR_LANGUAGE_NOT_AVAILABLE",
    }

    def __init__(self, status_code, lang_info):
        self.msg = self.error_codes.get(status_code) + " -> " + lang_info

    def __str__(self): return self.msg


class YandexHelper(TranslateBackendHelper):
    """YandexHelper - Handles Yandex Translation API requests"""

    def __init__(self, api_key):
        """Constructor for YandexHelper - Setup object with API key"""
        self.yandex_translate = YandexTranslator(api_key)
        self.available_languages = ['no', 'sv', 'sr', 'ro', 'mk', 'fi', 'ru',
                                    'cs', 'hu', 'hr', 'sl', 'sq', 'be', 'es',
                                    'tr', 'it', 'el', 'bg', 'pt', 'pl', 'uk',
                                    'hy', 'sk', 'ca', 'lv', 'nl', 'da', 'en',
                                    'de', 'fr', 'az', 'et', 'lt']
        self.available_translations = ['az-ru', 'be-bg', 'be-cs', 'be-de',
                                       'be-en', 'be-es', 'be-fr', 'be-it',
                                       'be-pl', 'be-ro', 'be-ru', 'be-sr',
                                       'be-tr', 'bg-be', 'bg-ru', 'bg-uk',
                                       'ca-en', 'ca-ru', 'cs-be', 'cs-en',
                                       'cs-ru', 'cs-uk', 'da-en', 'da-ru',
                                       'de-be', 'de-en', 'de-es', 'de-fr',
                                       'de-it', 'de-ru', 'de-tr', 'de-uk',
                                       'el-en', 'el-ru', 'en-be', 'en-ca',
                                       'en-cs', 'en-da', 'en-de', 'en-el',
                                       'en-es', 'en-et', 'en-fi', 'en-fr',
                                       'en-hu', 'en-it', 'en-lt', 'en-lv',
                                       'en-mk', 'en-nl', 'en-no', 'en-pt',
                                       'en-ru', 'en-sk', 'en-sl', 'en-sq',
                                       'en-sv', 'en-tr', 'en-uk', 'es-be',
                                       'es-de', 'es-en', 'es-ru', 'es-uk',
                                       'et-en', 'et-ru', 'fi-en', 'fi-ru',
                                       'fr-be', 'fr-de', 'fr-en', 'fr-ru',
                                       'fr-uk', 'hr-ru', 'hu-en', 'hu-ru',
                                       'hy-ru', 'it-be', 'it-de', 'it-en',
                                       'it-ru', 'it-uk', 'lt-en', 'lt-ru',
                                       'lv-en', 'lv-ru', 'mk-en', 'mk-ru',
                                       'nl-en', 'nl-ru', 'no-en', 'no-ru',
                                       'pl-be', 'pl-ru', 'pl-uk', 'pt-en',
                                       'pt-ru', 'ro-be', 'ro-ru', 'ro-uk',
                                       'ru-az', 'ru-be', 'ru-bg', 'ru-ca',
                                       'ru-cs', 'ru-da', 'ru-de', 'ru-el',
                                       'ru-en', 'ru-es', 'ru-et', 'ru-fi',
                                       'ru-fr', 'ru-hr', 'ru-hu', 'ru-hy',
                                       'ru-it', 'ru-lt', 'ru-lv', 'ru-mk',
                                       'ru-nl', 'ru-no', 'ru-pl', 'ru-pt',
                                       'ru-ro', 'ru-sk', 'ru-sl', 'ru-sq',
                                       'ru-sr', 'ru-sv', 'ru-tr', 'ru-uk',
                                       'sk-en', 'sk-ru', 'sl-en', 'sl-ru',
                                       'sq-en', 'sq-ru', 'sr-be', 'sr-ru',
                                       'sr-uk', 'sv-en', 'sv-ru', 'tr-be',
                                       'tr-de', 'tr-en', 'tr-ru', 'tr-uk',
                                       'uk-bg', 'uk-cs', 'uk-de', 'uk-en',
                                       'uk-es', 'uk-fr', 'uk-it', 'uk-pl',
                                       'uk-ro', 'uk-ru', 'uk-sr', 'uk-tr']

    def _detect_language(self, clipboard_content="Hello world!"):
        """Detects language of given text"""
        return self.yandex_translate.detect(clipboard_content)

    def _translation_available(self, source_lang, target_lang):
        translate_direction = source_lang + "-" + target_lang
        if source_lang == target_lang:
            raise YandexHelperException(406, translate_direction)
        if target_lang not in self.available_languages:
            print("[Error] Language not available!.")
            raise YandexHelperException(505, target_lang)
        if source_lang + "-" + target_lang not in self.available_translations:
            print("[Error] Translation not available!.")
            raise YandexHelperException(405, translate_direction)
        return True

    def _translate(self, clipboard_content, translate_direction):
        """Do the real translation"""
        return self.yandex_translate.translate(clipboard_content,
                                               translate_direction)

    def translate_auto(self, clipboard_content, target_lang):
        """Translates given content according to app preferences"""
        detected_language = self._detect_language(clipboard_content)
        translate_direction = detected_language + "-" + target_lang
        if self._translation_available(detected_language, target_lang):
            response = self._translate(clipboard_content, translate_direction)
            return response['text'][0]
        return "[Error] Language or translation not available!."

    def translate_manual(self, clipboard_content, source_lang, target_lang):
        """Translates given content according to given preferences"""
        if source_lang == "auto":
            return self.translate_auto(clipboard_content, target_lang)
        translate_direction = source_lang + "-" + target_lang
        if self._translation_available(source_lang, target_lang):
            response = self._translate(clipboard_content, translate_direction)
            return response['text'][0]
        return "[Error] Language or translation not available!."
