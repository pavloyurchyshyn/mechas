from settings.localization import LocalizationLoader, TEXT_PATH_DELIMITER


class LocalizationMixin:
    Delimiter = TEXT_PATH_DELIMITER
    PathSymbol = '@//'
    __localization = LocalizationLoader()

    def get_text_with_localization(self, text: str):
        if text.startswith(self.PathSymbol):
            return self.__localization.get_text(text.replace(self.PathSymbol, ''))
        else:
            return text

    @classmethod
    def build_path(cls, *args):
        return f'{cls.PathSymbol}{cls.Delimiter.join(args)}'
