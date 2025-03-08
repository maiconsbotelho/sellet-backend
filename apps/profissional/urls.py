from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfissionalViewSet

# Crie um roteador para registrar as views
router = DefaultRouter()

router.register(r'profissionais', ProfissionalViewSet)


# Inclua as URLs geradas pelo roteador
urlpatterns = [
    path('api/', include(router.urls)),  # Prefixo 'api/' para as rotas da API
]
