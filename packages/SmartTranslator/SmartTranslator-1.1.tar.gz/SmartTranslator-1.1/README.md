
## Smart Translator

***If the intelligent translation feature is enabled and the language of the user text matches the language
the user translates into, then the text is automatically translated into the default language***

***The ability to auto-check the text for errors***

**Using Smart Translation**

```
from smart_translator import SmartTranslate

translator = SmartTranslate()

print(translator.translate('Привет мир', 'ru'))
>>> Hello World
```
**Checking the spelling of the text**
```
from smart_translator import SmartTranslate

translator = SmartTranslate()

print(translator.auto_spelling('Hillo Wrld', 'ru').spelling_text)
# >>> Hello World
```
**Translation of the text corrected from errors**
```
from smart_translator import SmartTranslate

translator = SmartTranslate()

print(translator.auto_spelling('Hillo Wrld', 'ru').result)
# >>> Привет, мир
```
**All available languages**
```
from smart_translator import SmartTranslate

print(translator.LANGUAGES)
```
**Translation without using smart translation**
```
from smart_translator import SmartTranslate

translator = SmartTranslate(smart_translation=False)

print((translator.translate('Привет мир', 'ru')))
# >>> Привет мир
```
**Default language selection**
```
from smart_translator import SmartTranslate

translator = SmartTranslate(default_language='ru')

print((translator.translate('Hello World', 'en')))
# >>> Привет, мир
```