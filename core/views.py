from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tire, Appointment
import requests

def index(request):
    """
    Отображает главную страницу.
    Передаем варианты сезонов, чтобы отрисовать выпадающий список в фильтре.
    """
    seasons = Tire.SEASON_CHOICES

    context = {
        'seasons': seasons
    }
    return render(request, 'index.html', context)


def tire_catalog(request):
    """
    Отвечает за каталог и умный подбор шин.
    """
    # Сразу отсекаем шины, которых нет на складе (stock > 0)
    tires = Tire.objects.filter(stock__gt=0)

    # Ловим параметры, которые клиент ввел в форму поиска на сайте (GET-запрос)
    width = request.GET.get('width')
    profile = request.GET.get('profile')
    diameter = request.GET.get('diameter')
    season = request.GET.get('season')

    # Динамически фильтруем базу данных.
    # Если параметр передан — применяем фильтр, если нет — игнорируем.
    if width:
        tires = tires.filter(width=width)
    if profile:
        tires = tires.filter(profile=profile)
    if diameter:
        tires = tires.filter(diameter=diameter)
    if season and season != 'ALL': # Если выбрали конкретный сезон
        tires = tires.filter(season=season)

    context = {
        'tires': tires,
        'seasons': Tire.SEASON_CHOICES,
        # Возвращаем текущие параметры поиска обратно в шаблон,
        # чтобы значения в полях ввода не сбрасывались после перезагрузки
        'current_filters': request.GET
    }
    return render(request, 'catalog.html', context)


def send_telegram_message(name, phone, item, date):
    """
    Отправляет уведомление о новой заявке в Telegram бота.
    """
    # ВАЖНО: Вставь сюда свои данные!
    bot_token = '8568777588:AAFKl0C2y-lux54xLInATa9Jb-dx4K_1v6s'

    # Формируем красивое сообщение с эмодзи и HTML-тегами для жирного шрифта
    text = (
        f"🚨 <b>Новая заявка с сайта!</b>\n\n"
        f"👤 <b>Клиент:</b> {name}\n"
        f"📞 <b>Телефон:</b> {phone}\n"
        f"🔧 <b>Услуга/Товар:</b> {item}\n"
        f"📅 <b>Желаемая дата:</b> {date}\n"
    )

    # URL для обращения к API Telegram
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # Данные, которые мы отправляем
    data = {
        'text': text,
        'parse_mode': 'HTML' # Позволяет использовать <b> и <i> в тексте
    }

    # Пытаемся отправить запрос
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        # Если Telegram недоступен или нет интернета, сайт не должен упасть
        print(f"Ошибка отправки в Telegram: {e}")


# --- ОБНОВЛЕННЫЙ VIEW ДЛЯ ЗАПИСИ ---
def book_appointment(request):
    if request.method == 'POST':
        name = request.POST.get('customer_name')

        # Собираем и очищаем номер телефона
        raw_phone = request.POST.get('phone_number', '')
        clean_phone = '+998' + ''.join(filter(str.isdigit, raw_phone))

        item = request.POST.get('selected_item')
        date = request.POST.get('desired_date')

        # 1. Сохраняем лид в базу данных (в админку)
        Appointment.objects.create(
            customer_name=name,
            phone_number=clean_phone,
            selected_item=item,
            desired_date=date
        )

        # 2. ОТПРАВЛЯЕМ УВЕДОМЛЕНИЕ В ТЕЛЕГРАМ
        send_telegram_message(name, clean_phone, item, date)

        # Показываем сообщение об успехе
        messages.success(request, 'Отлично! Ваша заявка принята. Мы перезвоним для подтверждения.')

        return redirect('index')

    return render(request, 'contact.html')