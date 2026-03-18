from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=56)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='Services/')

class Tire(models.Model):
    # Варианты выбора для поля сезонности
    SEASON_CHOICES = [
        ('SUMMER', 'Лето'),
        ('WINTER', 'Зима'),
        ('ALL_SEASON', 'Всесезонка'),
    ]

    brand = models.CharField(max_length=100, verbose_name="Бренд")
    model_name = models.CharField(max_length=100, verbose_name="Модель")

    width = models.PositiveSmallIntegerField(verbose_name="Ширина")
    profile = models.PositiveSmallIntegerField(verbose_name="Профиль")
    diameter = models.PositiveSmallIntegerField(verbose_name="Диаметр (R)")

    season = models.CharField(max_length=20, choices=SEASON_CHOICES, verbose_name="Сезонность")

    stock = models.PositiveIntegerField(default=0, verbose_name="Наличие на складе (шт.)")

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.brand} {self.model_name} {self.width}/{self.profile} R{self.diameter}"

    class Meta:
        verbose_name = "Шина"
        verbose_name_plural = "Шины"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новая'),
        ('PROCESSING', 'В обработке'),
        ('COMPLETED', 'Завершена'),
    ]

    customer_name = models.CharField(max_length=150, verbose_name="Имя клиента")


    phone_number = models.CharField( max_length=17, verbose_name="Номер телефона")


    selected_item = models.CharField(max_length=255, verbose_name="Выбранная услуга или товар")

    desired_date = models.DateTimeField(verbose_name="Желаемая дата и время")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Статус заявки")


    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заявки")

    def __str__(self):
        return f"Заявка от {self.customer_name} (Статус: {self.get_status_display()})"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']
