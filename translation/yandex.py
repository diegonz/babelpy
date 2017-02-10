import requests

from translation.abc_translate import TranslateExceptionABC, TranslateHelperABC


class YandexTranslatorException(TranslateExceptionABC):
    """
    Default YandexTranslator exception
    """
    error_codes = {
        401: "ERR_KEY_INVALID",
        402: "ERR_KEY_BLOCKED",
        403: "ERR_DAILY_REQ_LIMIT_EXCEEDED",
        404: "ERR_DAILY_CHAR_LIMIT_EXCEEDED",
        413: "ERR_TEXT_TOO_LONG",
        422: "ERR_TEXT_NOT_PROCESSABLE",
        501: "ERR_LANG_NOT_SUPPORTED",
        503: "ERR_SERVICE_NOT_AVAILABLE",
    }

    def __init__(self, status_code):
        self.msg = self.error_codes.get(status_code)

    def __str__(self): return self.msg


class YandexTranslator(object):
    api_url = "https://translate.yandex.net/api/{version}/tr.json/{endpoint}"
    api_version = "v1.5"
    api_endpoints = {
        "langs": "getLangs",
        "detect": "detect",
        "translate": "translate",
    }

    def __init__(self, key=None):
        """
        >>> translate = YandexTranslator("API key here")
        >>> len(translate.api_endpoints)
        3
        """
        if not key:
            raise YandexTranslatorException(401)
        self.api_key = key

    def url(self, endpoint):
        """
        Returns full URL for specified API endpoint
        >>> translate = YandexTranslator("API key here")
        >>> translate.url("langs")
        'https://translate.yandex.net/api/v1.5/tr.json/getLangs'
        >>> translate.url("detect")
        'https://translate.yandex.net/api/v1.5/tr.json/detect'
        >>> translate.url("translate")
        'https://translate.yandex.net/api/v1.5/tr.json/translate'
        """
        return self.api_url.format(version=self.api_version,
                                   endpoint=self.api_endpoints[endpoint])

    @property
    def directions(self, proxies=None):
        """
        Returns list with translate directions
        >>> translate = YandexTranslator("API key here")
        >>> directions = translate.directions
        >>> len(directions) > 0
        True
        """
        try:
            response = requests.get(self.url("langs"),
                                    params={"key": self.api_key},
                                    proxies=proxies)
        except requests.exceptions.ConnectionError:
            error_code = YandexTranslatorException.error_codes[503]
            raise YandexTranslatorException(error_code)
        else:
            response = response.json()
        status_code = response.get("code", 200)
        if status_code != 200:
            raise YandexTranslatorException(status_code)
        return response.get("dirs")

    @property
    def langs(self):
        """
        Returns list with supported languages
        >>> translate = YandexTranslator("API key here")
        >>> languages = translate.langs
        >>> len(languages) > 0
        True
        """
        return set(x.split("-")[0] for x in self.directions)

    def detect(self, text, proxies=None, text_format="plain"):
        """
        Specifies language of text
        >>> translate = YandexTranslator("API key here")
        >>> result = translate.detect(text="Hello world!")
        >>> result == "en"
        True
        """
        data = {
            "text": text,
            "format": text_format,
            "key": self.api_key,
        }
        try:
            response = requests.post(self.url("detect"), data=data,
                                     proxies=proxies)
        except ConnectionError:
            error_code = YandexTranslatorException.error_codes[503]
            raise YandexTranslatorException(error_code)
        except ValueError:
            error_code = YandexTranslatorException.error_codes[422]
            raise YandexTranslatorException(error_code)
        else:
            response = response.json()
        language = response.get("lang", None)
        status_code = response.get("code", 200)
        if status_code != 200:
            raise YandexTranslatorException(status_code)
        elif not language:
            raise YandexTranslatorException(501)
        return language

    def translate(self, text, lang, proxies=None, text_format="plain"):
        """
        Translates text to passed language
        >>> translate = YandexTranslator("API key here")
        >>> result = translate.translate(lang="ru", text="Hello, world!")
        >>> result["code"] == 200
        True
        >>> result["lang"] == "en-ru"
        True
        """
        data = {
            "text": text,
            "format": text_format,
            "lang": lang,
            "key": self.api_key
        }
        try:
            response = requests.post(self.url("translate"), data=data,
                                     proxies=proxies)
        except ConnectionError:
            raise YandexTranslatorException(503)
        else:
            response = response.json()
        status_code = response.get("code", 200)
        if status_code != 200:
            raise YandexTranslatorException(status_code)
        return response


class YandexHelperException(TranslateExceptionABC):
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


class YandexHelper(TranslateHelperABC):
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
