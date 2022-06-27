import yaml
from os import listdir
from settings.global_parameters import get_language
from settings.base import LOCALIZATIONS_FOLDER
from common.logger import Logger
from common.singleton import Singleton

LOGGER = Logger()

NO_TEXT_MSG = 'no text'

TEXT_PATH_DELIMITER = '/./'
__all__ = ['LocalizationLoader', 'LOCAL', 'TEXT_PATH_DELIMITER']


class TextValue:
    def __init__(self, value):
        self.value = value

    def __getattr__(self, name):
        return NO_TEXT_MSG


class LocalizationConfig:
    pattern = '{}\\{}.yaml'

    def __init__(self, language: str):
        self.country = language
        self.load()

    def load(self):
        LOGGER.info(f'Importing localization {self.country.upper()}')
        with open(self.pattern.format(LOCALIZATIONS_FOLDER, self.country), encoding='utf8') as f:
            local_ = yaml.safe_load(f)
        for k, val in local_.items():
            if type(val) is not dict:
                setattr(self, k, val)
            else:
                self.parse_dict(k, val, self)

    @staticmethod
    def parse_dict(key, value: dict, prev_obj):
        obj = TextValue(key)
        setattr(prev_obj, key, obj)
        for k, v in value.items():
            if type(v) is not dict:
                setattr(obj, k, v)
            else:
                LocalizationConfig.parse_dict(k, v, obj)

    def __getattr__(self, name):
        return NO_TEXT_MSG


class LocalizationLoader(metaclass=Singleton):
    def __init__(self):
        self.available_langs = [l.replace('.yaml', '') for l in listdir(LOCALIZATIONS_FOLDER) if l.endswith('.yaml')]
        self._current_language = get_language()
        self.load_lang('eng')
        self.load_current_lang()

    def change_language(self, lang):
        self._current_language = lang

    @property
    def text(self):
        return getattr(self, self._current_language)

    def load_lang(self, lang):
        LOGGER.info(f'Loading {lang} language')
        setattr(self, lang, LocalizationConfig(lang))
        LOGGER.info(f'Language {lang} successfully loaded.')

    def load_current_lang(self):
        self.load_lang(self._current_language)

    def get_text(self, path):
        # LOGGER.info(f'Searching localization for {path}')
        text = self.text
        for attr in path.split(TEXT_PATH_DELIMITER):
            text = getattr(text, attr)
            if text == NO_TEXT_MSG:
                return text

        return text

    def __getattr__(self, name):
        return NO_TEXT_MSG


LOCAL = LocalizationLoader()

if __name__ == '__main__':
    l = LocalizationLoader()
    print(l.__dict__)
