from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Plant(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='plants',
        verbose_name='Владелец',
    )
    name = models.CharField('Имя растения', max_length=100)
    species = models.CharField('Вид / сорт', max_length=100, blank=True)
    photo = models.ImageField('Фото', upload_to='plants/', blank=True, null=True)
    watering_interval_days = models.PositiveIntegerField(
        'Интервал полива (дней)', default=7
    )
    last_watered = models.DateField('Последний полив', default=date.today)
    notes = models.TextField('Заметки', blank=True)
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        ordering = ['last_watered']
        verbose_name = 'Растение'
        verbose_name_plural = 'Растения'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plant_detail', kwargs={'pk': self.pk})

    def next_water_date(self):
        return self.last_watered + timedelta(days=self.watering_interval_days)

    def days_until_watering(self):
        return (self.next_water_date() - date.today()).days

    def status(self):
        days = self.days_until_watering()
        if days < 0:
            return 'overdue'
        if days == 0:
            return 'today'
        return 'ok'

    def overdue_days(self):
        return max(0, -self.days_until_watering())
