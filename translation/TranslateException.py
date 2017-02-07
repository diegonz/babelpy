from abc import ABC


class TranslateException(ABC, Exception):
    """TranslateException: Abstract class representing translate exception"""
    error_codes = {
        401: "ERR_KEY_INVALID",
        402: "ERR_KEY_BLOCKED",
        403: "ERR_DAILY_REQ_LIMIT_EXCEEDED",
        404: "ERR_DAILY_CHAR_LIMIT_EXCEEDED",
        405: "ERR_TRANSLATION_NOT_AVAILABLE",
        406: "ERR_SAME_LANGUAGE_SOURCE_AND_TARGET",
        413: "ERR_TEXT_TOO_LONG",
        422: "ERR_TEXT_NOT_PROCESSABLE",
        501: "ERR_LANG_NOT_SUPPORTED",
        503: "ERR_SERVICE_NOT_AVAILABLE",
        505: "ERR_LANGUAGE_NOT_AVAILABLE",
    }

    def __init__(self, status_code, *args, **kwargs):
        message = self.error_codes.get(status_code)
        super(TranslateException, self).__init__(message, *args,
                                                 **kwargs)
