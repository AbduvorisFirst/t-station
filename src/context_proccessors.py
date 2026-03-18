from core.translations import TEXTS

def multi_lang(request):
    lang = request.session.get('lang', 'ru')
    return {
        't': TEXTS.get(lang, TEXTS['ru']),
        'current_lang': lang
    }