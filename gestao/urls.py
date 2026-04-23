from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .api_views import DeviceViewSet, RackViewSet, SalaViewSet, TelemetryLogViewSet

app_name = 'gestao' # namespace para referenciar rotas como 'gestao:home'

# Configuração do Router para a API
router = DefaultRouter()
router.register(r'salas', SalaViewSet)
router.register(r'racks', RackViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'logs', TelemetryLogViewSet)

urlpatterns = [
    # VISÃO GERAL E NAVEGAÇÃO
    path('', views.home, name='home'),
    path('salas/<int:pk>/', views.sala_detalhe, name='sala_detalhe'),
    path('racks/<int:pk>/', views.rack_detalhe, name='rack_detalhe'),
    path('devices/<int:pk>/', views.device_detalhe, name='device_detalhe'),

    # CRUD DE SALAS 
    path('sala/nova/', views.sala_criar, name='sala_criar'),
    path('sala/<int:pk>/editar/', views.sala_editar, name='sala_editar'),
    path('sala/<int:pk>/deletar/', views.sala_deletar, name='sala_deletar'),

    # CRUD DE RACKS
    path('rack/novo/', views.rack_criar, name='rack_criar'),
    path('rack/<int:pk>/editar/', views.rack_editar, name='rack_editar'),
    path('rack/<int:pk>/deletar/', views.rack_deletar, name='rack_deletar'),

    # CRUD de devices
    path('devices/gerenciar/', views.device_gerenciar, name='device_gerenciar'),
    path('devices/novo/', views.device_novo, name='device_novo'),
    path('devices/<int:pk>/editar/', views.device_editar, name='device_editar'),
    path('devices/<int:pk>/excluir/', views.device_excluir, name='device_excluir'), 

    # API ENDPOINTS
    path('api/', include(router.urls)),
]
