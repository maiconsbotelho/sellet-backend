from django.urls import path
from .views import RelatorioAgendamentosView, RelatorioServicosView

urlpatterns = [
    path('relatorio/agendamentos/', RelatorioAgendamentosView.as_view(), name='relatorio-agendamentos'),
    path('relatorio/servicos/', RelatorioServicosView.as_view(), name='relatorio-servicos'),
]
