# babelPY

A command line tool to translate text from the clipboard or selected text.

## Config file

Example of a simple config file (default `~/.babelPy.json`) containing _all_ the config entries:

```json
{
  "babelPY": "Config settings file for babelPy",
  "default_backend": "backend",
  "available_backend": {
    "yandex": {
      "api_key": "YourYandexApiKey"
    },
    "microsoft": {
      "api_key": "YourMicrosoftApiKey"
    },
    "google": {
      "api_key": "YourGoogleApiKey"
    }
  },
  "default_language": "en",
  "default_input": "clipboard",
  "default_output": "notify",
  "default_exchange": false
}
```

## Usage examples

You can simply run `babelPy` to run translation, picking preferences from default config file (`~/.babelPy.json`).

Example of `babelPY -h` or `babelPy --help`  output:

```bash
usage: babelPy.py [-h] [-a [YourApiKey]] [-b [yandex|other]]
                  [-c [.babelPy.json]] [-s [en|es]] [-t [en|es]]
                  [-m [Text to translate]] [-i [clipboard|selection]]
                  [-o [stdout|notify|dialog|none]] [-x] [--save-config]

An easy tool for those who would not survive in the tower of Babel

optional arguments:
  -h, --help            show this help message and exit
  -a [YourApiKey], --api-key [YourApiKey]
                        Your API key for target (or default) backend
  -b [yandex|other], --backend [yandex|other]
                        Target translate backend (Default: yandex)
  -c [.babelPy.json], --config-file [.babelPy.json]
                        Path to config file (load and save)
  -s [en|es], --source-lang [en|es]
                        Give a source language (avoids auto detection)
  -t [en|es], --target-lang [en|es]
                        Give a target language (overrides config)
  -m [Text to translate], --message [Text to translate]
                        Pass directly the actual text to translate as an
                        argument (overrides clipboard and selection)
  -i [clipboard|selection], --input [clipboard|selection]
                        From where the text has to be taken
  -o [stdout|notify|dialog|none], --output [stdout|notify|dialog|none]
                        Where to (out)put the translation
  -x, --exchange        Exchange/paste translation to clipboard
  --save-config         Save a config file at default (or -c given) path,
                        based on default or stored/saved settings.

Enjoy!
```
