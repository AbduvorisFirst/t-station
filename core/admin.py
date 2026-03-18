from django.contrib import admin
from .models import Tire, Appointment

# Кастомизация заголовков самой админ-панели (чтобы было стильно)
admin.site.site_header = "Управление Автосервисом"
admin.site.site_title = "Панель администратора"
admin.site.index_title = "Добро пожаловать в панель управления"

@admin.register(Tire)
class TireAdmin(admin.ModelAdmin):
    # 1. Что показываем в виде колонок в общем списке
    list_display = ('brand', 'model_name', 'get_size', 'season', 'stock', 'price')

    # 2. ДЕЛАЕМ КРУТУЮ ФИШКУ: Редактирование прямо из списка!
    # Владелец сможет менять цену и остатки на складе в один клик
    list_editable = ('stock', 'price')

    # 3. Боковая панель для быстрой фильтрации (например, показать только зимние шины)
    list_filter = ('season', 'brand', 'diameter')

    # 4. Поиск по бренду и модели
    search_fields = ('brand', 'model_name')

    # 5. Красивая группировка полей внутри карточки товара
    fieldsets = (
        ('Основная информация', {
            'fields': ('brand', 'model_name', 'season')
        }),
        ('Размеры', {
            'fields': ('width', 'profile', 'diameter')
        }),
        ('Склад и финансы', {
            'fields': ('stock', 'price')
        }),
    )

    # Кастомный метод, чтобы красиво склеить размеры в одну колонку (например: 205/55 R16)
    @admin.display(description='Размер')
    def get_size(self, obj):
        return f"{obj.width}/{obj.profile} R{obj.diameter}"


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # Колонки для списка заявок
    list_display = ('customer_name', 'phone_number', 'status', 'desired_date', 'created_at')

    # Возможность быстро поменять статус заявки на "Завершена" или "В обработке"
    list_editable = ('status',)

    # Фильтр по статусу и дате
    list_filter = ('status', 'desired_date', 'created_at')

    # Поиск по имени клиента и номеру телефона
    search_fields = ('customer_name', 'phone_number', 'selected_item')

    # Запрещаем редактировать дату создания заявки (это системное поле)
    readonly_fields = ('created_at',)

    # Группировка блоков в карточке заявки
    fieldsets = (
        ('Данные клиента', {
            'fields': ('customer_name', 'phone_number')
        }),
        ('Детали заказа', {
            'fields': ('selected_item', 'desired_date', 'status')
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',) # Эта настройка скроет блок под кат, чтобы не мешался
        }),
    )