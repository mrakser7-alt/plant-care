from django.contrib import admin

from .models import Plant, PlantType


@admin.register(PlantType)
class PlantTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'latin_name', 'icon', 'watering_interval_days', 'repotting_interval_days')
    search_fields = ('name', 'latin_name')


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'plant_type', 'is_alive', 'last_watered', 'last_repotted')
    list_filter = ('user', 'plant_type', 'is_alive')
    search_fields = ('name',)
