from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet

# Crie um roteador para registrar as views
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)


# Inclua as URLs geradas pelo roteador
urlpatterns = [
    path('api/', include(router.urls)),  # Prefixo 'api/' para as rotas da API
]






