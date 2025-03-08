from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes/', include('apps.cliente.urls')),  # Inclui as rotas do app cliente
    path('agendamentos/', include('apps.agendamento.urls')),
    path('servicos/', include('apps.servico.urls')),
    path('profissionais/', include('apps.profissional.urls')),
]
