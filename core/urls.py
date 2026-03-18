from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Главная страница: http://твоисайт.com/
    path('catalog/', views.tire_catalog, name='catalog'), # Каталог: http://твоисайт.com/catalog/
    path('contact/', views.book_appointment, name='contact'),
    path('lang/<str:lang_code>/', views.change_language, name='change_lang'),
]