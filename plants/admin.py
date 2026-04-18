from django.contrib import admin

from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'species', 'last_watered', 'watering_interval_days')
    list_filter = ('user',)
    search_fields = ('name', 'species')
