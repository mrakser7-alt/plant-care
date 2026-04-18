# главный роутер проекта - распределяет запросы по приложениям
# всё что после домена идёт сюда

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # встроенная админка
    path('admin/', admin.site.urls),
    # наша регистрация
    path('accounts/', include('accounts.urls')),
    # встроенный логин/логаут/смена пароля
    path('accounts/', include('django.contrib.auth.urls')),
    # всё остальное - приложение plants
    path('', include('plants.urls')),
]

# чтобы фото (media/) отдавались в дев-режиме
# в проде так нельзя, но тут нам норм
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
