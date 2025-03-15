from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet


router = DefaultRouter() # Crie um roteador para registrar as views
router.register(r'', ClienteViewSet) # Registre a view de cliente


# Inclua as URLs geradas pelo roteador
urlpatterns = [
    path('', include(router.urls)),  # Prefixo 'api/' para as rotas da API
]






