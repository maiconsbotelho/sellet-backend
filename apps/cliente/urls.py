from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet

# Crie um roteador para registrar as views
router = DefaultRouter()
router.register(r'', ClienteViewSet)


# Inclua as URLs geradas pelo roteador
urlpatterns = [
    path('', include(router.urls)),  # Prefixo 'api/' para as rotas da API
]






