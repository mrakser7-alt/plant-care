# вьюхи - это функции которые обрабатывают запросы
# каждая вьюха получает request, что-то делает и возвращает HttpResponse или редирект

from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PlantForm
from .models import Plant


# главная страница - список растений юзера
# @login_required = если не залогинен, кинет на страницу входа
@login_required
def dashboard(request):
    # берём растения только текущего юзера
    # select_related = сразу подтягивает PlantType одним запросом (чтобы быстрее)
    plants = request.user.plants.select_related('plant_type').all()
    return render(request, 'plants/dashboard.html', {'plants': plants})


# страница одного растения
@login_required
def plant_detail(request, pk):
    # get_object_or_404 = если нет такого, покажет 404
    # фильтр user=request.user чтобы нельзя было смотреть чужие растения
    plant = get_object_or_404(
        Plant.objects.select_related('plant_type'), pk=pk, user=request.user
    )
    return render(request, 'plants/plant_detail.html', {'plant': plant})


# добавить растение
@login_required
def plant_create(request):
    if request.method == 'POST':
        # request.FILES нужен потому что форма грузит фото
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False = создать объект но пока не сохранять в базу
            # нам нужно сначала проставить user
            plant = form.save(commit=False)
            plant.user = request.user
            plant.save()
            return redirect('dashboard')
    else:
        form = PlantForm()
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Новое растение'})


# редактирование
@login_required
def plant_update(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    if request.method == 'POST':
        # instance=plant = форма заполнится текущими данными
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plant_detail', pk=plant.pk)
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Изменить растение'})


# удаление - GET показывает подтверждение, POST реально удаляет
@login_required
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    if request.method == 'POST':
        plant.delete()
        return redirect('dashboard')
    return render(request, 'plants/plant_confirm_delete.html', {'plant': plant})


# кнопка "я полил" - обновляем дату полива на сегодня
# require_POST = можно дёргать только POSTом, чтобы случайно не полить по клику по ссылке
@login_required
@require_POST
def water_plant(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    plant.last_watered = date.today()
    # update_fields = сохраняем только это поле, остальное не трогаем
    plant.save(update_fields=['last_watered'])
    # возвращаем туда откуда пришли (или на dashboard если реферера нет)
    return redirect(request.META.get('HTTP_REFERER') or 'dashboard')


# кнопка "пересадил"
@login_required
@require_POST
def repot_plant(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    plant.last_repotted = date.today()
    plant.save(update_fields=['last_repotted'])
    return redirect(request.META.get('HTTP_REFERER') or 'dashboard')


# переключатель "живо/погибло"
@login_required
@require_POST
def toggle_alive(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    plant.is_alive = not plant.is_alive
    plant.save(update_fields=['is_alive'])
    return redirect(request.META.get('HTTP_REFERER') or 'dashboard')
