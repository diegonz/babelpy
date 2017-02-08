import json
import os


class ConfigSettings:
    """ConfigSettings - Util class for handling config settings"""

    def __init__(self, config_file_path):
        """Constructor for ConfigSettings - Loads config settings from file"""
        self.config_path = config_file_path
        try:
            with open(config_file_path) as config_file:
                loaded_data = json.load(config_file)
                self.backend = loaded_data['default_backend']
                self.language = loaded_data['default_language']
                self.input = loaded_data['default_input']
                self.output = loaded_data['default_output']
                self.exchange = loaded_data['default_exchange']
                self.yandex_api_key = loaded_data['backend']['yandex'][
                    'api_key']
                self.microsoft_api_key = loaded_data['backend']['microsoft'][
                    'api_key']
                self.google_api_key = loaded_data['backend']['google'][
                    'api_key']
                self.api_key = loaded_data['backend'][self.backend]['api_key']
        except FileNotFoundError:
            print("[Warning] No config file found, creating empty settings...")
            self.backend = "yandex"
            self.language = "en"
            self.input = "clipboard"
            self.output = "notify"
            self.exchange = False
            # TODO Empty api_key before publishing
            self.api_key = 'trnsl.1.1.20170203T202734Z.5093fb80fddda4' \
                           '6a.b66dd1bf1599f71e29ca9f3afe38d9a5ac9fc216'
            self.yandex_api_key = ""
            self.microsoft_api_key = ""
            self.google_api_key = ""

    def save(self, parsed_args):
        """save - Saves config settings to given file"""
        print(parsed_args)
        print(self.api_key)
        if parsed_args.backend == "yandex":
            self.backend = parsed_args.backend
            if parsed_args.api_key:
                self.yandex_api_key = parsed_args.api_key
        elif parsed_args.backend == "microsoft":
            self.backend = parsed_args.backend
            if parsed_args.api_key:
                self.microsoft_api_key = parsed_args.api_key
        elif parsed_args.backend == "google":
            self.backend = parsed_args.backend
            if parsed_args.api_key:
                self.google_api_key = parsed_args.api_key

        if self.api_key:
            if self.backend == "yandex":
                self.yandex_api_key = self.api_key
            elif self.backend == "microsoft":
                self.microsoft_api_key = self.api_key
            elif self.backend == "google":
                self.google_api_key = self.api_key

        if parsed_args.source_lang:
            self.language = parsed_args.source_lang
        if parsed_args.input:
            self.input = parsed_args.input
        if parsed_args.output:
            self.output = parsed_args.output
        if parsed_args.exchange:
            self.exchange = parsed_args.exchange
        try:
            with open(self.config_path, 'w') as config_file:
                json.dump(
                    {"babelPY": "Config settings file for babelPy",
                     "default_backend": self.backend,
                     "backend": {
                         "yandex": {"api_key": self.yandex_api_key},
                         "microsoft": {"api_key": self.microsoft_api_key},
                         "google": {"api_key": self.google_api_key}
                     },
                     "default_language": self.language,
                     "default_input": self.input,
                     "default_output": self.output,
                     "default_exchange": self.exchange},
                    config_file)
                print("Settings successfully saved at: " + config_file.name)
                return 0  # Status code to return to sys.exit()
        except (OSError, IOError) as exception:
            print("[Error] There was an IO error while writing config file!")
            print("[Error] -> " + exception.errno)
            print("[Error code] -> " + exception.errorcode[exception.errno])
            print("[Error message] -> " + os.strerror(exception.errno))
            return 1  # Status code to return to sys.exit()
