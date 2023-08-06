from smart_translator import SmartTranslate

translator = SmartTranslate()

# Using Smart Translation
print(translator.translate('Привет мир', 'ru'))
# >>> Hello World

# Checking the spelling of the text
print(translator.auto_spelling('Hillo Wrld', 'ru').spelling_text)
# >>> Hello World

# Translation of the text corrected from errors
print(translator.auto_spelling('Hillo Wrld', 'ru').result)
# >>> Привет, мир

print(translator.LANGUAGES)
# >>> All available languages


# translation without using smart translation
translator = SmartTranslate(smart_translation=False)
print((translator.translate('Привет мир', 'ru')))
# >>> Привет мир


# Default language selection
translator = SmartTranslate(default_language='ru')
print((translator.translate('Hello World', 'en')))
# >>> Привет, мир