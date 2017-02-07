#!/usr/bin/env python3

# coding: utf-8

import unittest
from translation.yandex.yandex_translator import YandexTranslator, \
    YandexTranslatorException


# noinspection SpellCheckingInspection
class YandexTranslatorTest(unittest.TestCase):
    def setUp(self):
        self.translate = YandexTranslator("trnsl.1.1.20130421T140201Z.323e508a"
                                         "33e9d84b.f1e0d9ca9bcd0a00b0ef71d82e"
                                         "6cf4158183d09e")

    def test_directions(self):
        directions = self.translate.directions
        self.assertGreater(len(directions), 1)

    def test_langs(self):
        languages = self.translate.langs
        self.assertEqual(languages,
                         {u"el", u"en", u"ca", u"it", u"hy", u"cs", u"et",
                          u"az", u"es", u"ru", u"nl", u"pt", u"no", u"tr",
                          u"lv", u"lt", u"ro", u"pl", u"be", u"fr", u"bg",
                          u"hr", u"de", u"da", u"fi", u"hu", u"sr", u"sq",
                          u"sv", u"mk", u"sk", u"uk", u"sl"})

    def test_blocked_key(self):
        translate = YandexTranslator("trnsl.1.1.20130723T112255Z.cfcd2b1ebae9f"
                                    "ff1.86f3d1de3621e69b8c432fcdd6803bb87ef0"
                                    "e963")
        with self.assertRaises(YandexTranslatorException,
                               msg="ERR_KEY_BLOCKED"):
            translate.detect("Hello world!")

    def test_detect_language(self):
        language = self.translate.detect(text="This is a test!")
        self.assertEqual(language, "en")

    def test_translate(self):
        result = self.translate.translate(u"Hello", "es")
        self.assertEqual(result["text"][0], u"Hola")
        self.assertEqual(result["code"], 200)

    def test_translate_in_another_direction(self):
        result = self.translate.translate(u"Hola", "en")
        self.assertEqual(result["text"][0], u"Hello")
        self.assertEqual(result["code"], 200)

    def test_without_key(self):
        with self.assertRaises(YandexTranslatorException,
                               msg="Please, provide key for "
                                   "Yandex.Translate API: "
                                   "https://translate.yandex.ru/apikeys"):
            YandexTranslator()

    def test_error_long_text(self):
        with self.assertRaises(YandexTranslatorException,
                               msg="ERR_TEXT_TOO_LONG"):
            self.translate.translate("Hello world! " * 4098, "es")

    def test_invalid_key(self):
        with self.assertRaises(YandexTranslatorException,
                               msg="ERR_KEY_INVALID"):
            translate = YandexTranslator("my-invalid-key")
            translate.detect("Hello world!")

if __name__ == "__main__":
    unittest.main()
