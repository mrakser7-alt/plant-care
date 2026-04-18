from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PlantForm
from .models import Plant


@login_required
def dashboard(request):
    plants = request.user.plants.select_related('plant_type').all()
    return render(request, 'plants/dashboard.html', {'plants': plants})


@login_required
def plant_detail(request, pk):
    plant = get_object_or_404(Plant.objects.select_related('plant_type'), pk=pk, user=request.user)
    return render(request, 'plants/plant_detail.html', {'plant': plant})


@login_required
def plant_create(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.user = request.user
            plant.save()
            return redirect('dashboard')
    else:
        form = PlantForm()
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Новое растение'})


@login_required
def plant_update(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('plant_detail', pk=plant.pk)
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Изменить растение'})


@login_required
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    if request.method == 'POST':
        plant.delete()
        return redirect('dashboard')
    return render(request, 'plants/plant_confirm_delete.html', {'plant': plant})


@login_required
@require_POST
def water_plant(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    plant.last_watered = date.today()
    plant.save(update_fields=['last_watered'])
    return redirect(request.META.get('HTTP_REFERER') or 'dashboard')


@login_required
@require_POST
def repot_plant(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    plant.last_repotted = date.today()
    plant.save(update_fields=['last_repotted'])
    return redirect(request.META.get('HTTP_REFERER') or 'dashboard')


@login_required
@require_POST
def toggle_alive(request, pk):
    plant = get_object_or_404(Plant, pk=pk, user=request.user)
    plant.is_alive = not plant.is_alive
    plant.save(update_fields=['is_alive'])
    return redirect(request.META.get('HTTP_REFERER') or 'dashboard')
