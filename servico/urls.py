from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServicoViewSet

# Crie um roteador para registrar as views
router = DefaultRouter()
router.register(r'servicos', ServicoViewSet)

# Inclua as URLs geradas pelo roteador
urlpatterns = [
    path('api/', include(router.urls)),  # Prefixo 'api/' para as rotas da API
]
