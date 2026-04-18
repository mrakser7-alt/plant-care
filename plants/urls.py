# url-ы приложения plants
# каждая строка говорит: "когда юзер идёт по такому адресу - вызывай такую вьюху"

from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('plants/add/', views.plant_create, name='plant_create'),
    path('plants/<int:pk>/', views.plant_detail, name='plant_detail'),
    path('plants/<int:pk>/edit/', views.plant_update, name='plant_update'),
    path('plants/<int:pk>/delete/', views.plant_delete, name='plant_delete'),
    # эти три - кнопки-действия, дёргаются только POSTом
    path('plants/<int:pk>/water/', views.water_plant, name='water_plant'),
    path('plants/<int:pk>/repot/', views.repot_plant, name='repot_plant'),
    path('plants/<int:pk>/toggle-alive/', views.toggle_alive, name='toggle_alive'),
]
