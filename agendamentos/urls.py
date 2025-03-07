from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, ProfissionalViewSet, ServicoViewSet, AgendamentoViewSet

# Crie um roteador para registrar as views
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'profissionais', ProfissionalViewSet)
router.register(r'servicos', ServicoViewSet)
router.register(r'agendamentos', AgendamentoViewSet)

# Inclua as URLs geradas pelo roteador
urlpatterns = [
    path('api/', include(router.urls)),  # Prefixo 'api/' para as rotas da API
]
