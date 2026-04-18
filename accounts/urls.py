# url-ы приложения accounts (регистрация)
# login/logout лежат в django.contrib.auth.urls, подключены в plantcare/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
]
