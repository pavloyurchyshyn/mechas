from settings.localization import LocalizationLoader, TEXT_PATH_DELIMITER


class LocalizationMixin:
    Delimiter = TEXT_PATH_DELIMITER
    PathSymbol = '@//'
    __localization = LocalizationLoader()

    @staticmethod
    def get_text_with_localization(text: str):
        if text.startswith(LocalizationMixin.PathSymbol):
            return LocalizationMixin.__localization.get_text(text.replace(LocalizationMixin.PathSymbol, ''))
        else:
            return text

    @classmethod
    def build_path(cls, *args):
        return f'{cls.PathSymbol}{cls.Delimiter.join(args)}'
