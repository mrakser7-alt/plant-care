from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class PlantType(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    latin_name = models.CharField('Латинское название', max_length=100, blank=True)
    icon = models.CharField('Иконка (эмодзи)', max_length=4, default='🌱')
    watering_interval_days = models.PositiveIntegerField('Интервал полива (дней)', default=7)
    repotting_interval_days = models.PositiveIntegerField('Интервал пересадки (дней)', default=730)
    description = models.TextField('Описание', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Вид растения'
        verbose_name_plural = 'Виды растений'

    def __str__(self):
        return f'{self.icon} {self.name}'


class Plant(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='plants', verbose_name='Владелец',
    )
    plant_type = models.ForeignKey(
        PlantType, on_delete=models.PROTECT, related_name='plants', verbose_name='Вид',
    )
    name = models.CharField('Имя растения', max_length=100)
    photo = models.ImageField('Фото', upload_to='plants/', blank=True, null=True)
    last_watered = models.DateField('Последний полив', default=date.today)
    last_repotted = models.DateField('Последняя пересадка', default=date.today)
    is_alive = models.BooleanField('Живо', default=True)
    notes = models.TextField('Заметки', blank=True)
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        ordering = ['-is_alive', 'last_watered']
        verbose_name = 'Растение'
        verbose_name_plural = 'Растения'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plant_detail', kwargs={'pk': self.pk})

    def next_water_date(self):
        return self.last_watered + timedelta(days=self.plant_type.watering_interval_days)

    def days_until_watering(self):
        return (self.next_water_date() - date.today()).days

    def next_repot_date(self):
        return self.last_repotted + timedelta(days=self.plant_type.repotting_interval_days)

    def days_until_repotting(self):
        return (self.next_repot_date() - date.today()).days

    def overdue_days(self):
        return max(0, -self.days_until_watering())

    def status(self):
        if not self.is_alive:
            return 'dead'
        water_days = self.days_until_watering()
        if water_days < -3:
            return 'dry'
        if water_days < 0:
            return 'overdue'
        if water_days == 0:
            return 'today'
        if self.days_until_repotting() <= 0:
            return 'needs_repot'
        return 'ok'

    def status_label(self):
        return {
            'dead': '💀 Погибло',
            'dry': '🏜️ Сухой! Срочно полить',
            'overdue': f'🔴 Просрочено на {self.overdue_days()} дн.',
            'today': '🟡 Полить сегодня!',
            'needs_repot': '🪴 Пора пересаживать',
            'ok': f'🟢 Полить через {self.days_until_watering()} дн.',
        }[self.status()]

    def status_css(self):
        return {
            'dead': 'bg-secondary',
            'dry': 'bg-danger',
            'overdue': 'bg-danger',
            'today': 'bg-warning text-dark',
            'needs_repot': 'bg-info text-dark',
            'ok': 'bg-success',
        }[self.status()]
