from googletrans import Translator, LANGUAGES
from pyaspeller import YandexSpeller


class Translate:

    def __init__(self):
        self.translator = Translator()
        self.LANGUAGES = LANGUAGES
        self.spelling = YandexSpeller()
        self.default_language = 'en'

    def translate(self, text, language, smart_translation=True) -> str:

        """
        Logic
        ___________
        if the smart translation function is enabled and the language of the user's text matches the language
        into which the user translates, then the text is translated into English automatically

        the default language can be selected

        Returns
        ___________
        User text translation

        """

        text = "No Text" if text == '' else text

        result = self.translator.translate(text, dest=language)

        if result.src == language and smart_translation:
            return self.translator.translate(text, dest=self.default_language).text
        else:
            return result.text

    def auto_spelling(self, text, language):

        """
        Logic
        ___________
        check the spelling of the text, correct errors

        Returns
        ___________
        translation of the corrected text
        """

        # Corrected text
        spelling_text = self.spelling.spelled(text)
        # Translation of the corrected text
        result = self.translate(spelling_text, language)

        return AutoSpelling(spelling_text, result)


class AutoSpelling:
    def __init__(self, spelling_text, result):
        self.spelling_text = spelling_text
        self.result = result

    def __dict__(self):
        return {'spelling_text': self.spelling_text,
                'result': self.result}