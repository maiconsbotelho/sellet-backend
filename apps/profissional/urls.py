from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfissionalViewSet

# Crie um roteador para registrar as views
router = DefaultRouter()

router.register(r'', ProfissionalViewSet)


# Inclua as URLs geradas pelo roteador
urlpatterns = [
    path('', include(router.urls)),  # Prefixo 'api/' para as rotas da API
]
