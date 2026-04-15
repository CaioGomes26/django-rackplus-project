from django.urls import path

from . import views

app_name = 'gestao'  # namespace para referenciar rotas como 'gestao:home'

urlpatterns = [
    # Visão geral e navegação hierárquica
    path('', views.home, name='home'),
    path('salas/<int:pk>/', views.sala_detalhe, name='sala_detalhe'),
    path('racks/<int:pk>/', views.rack_detalhe, name='rack_detalhe'),
    path('devices/<int:pk>/', views.device_detalhe, name='device_detalhe'),

    # CRUD de devices
    path('devices/gerenciar/', views.device_gerenciar, name='device_gerenciar'),
    path('devices/novo/', views.device_novo, name='device_novo'),
    path('devices/<int:pk>/editar/', views.device_editar, name='device_editar'),
    path('devices/<int:pk>/excluir/', views.device_excluir, name='device_excluir'),
]