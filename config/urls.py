from django.contrib import admin
from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('clientes/', include('apps.cliente.urls')),  # Inclui as rotas do app cliente
#     path('agendamentos/', include('apps.agendamento.urls')),
#     path('servicos/', include('apps.servico.urls')),
#     path('profissionais/', include('apps.profissional.urls')),
# ]

# meu_projeto/urls.py

urlpatterns = [
    # Outras URLs da sua API
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Endpoint para obter o token
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Endpoint para atualizar o token
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),
    path('api/', include('servicos.urls')), 
    path('api/', include('agendamentos.urls')),
]
