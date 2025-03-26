from django.contrib import admin
from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.urls')),  # API de usuários
    path('api/servicos/', include('servicos.urls')),  # API de serviços
    path('api/agendamentos/', include('agendamentos.urls')),  # API de agendamentos

    # Outros endpoints da sua API
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Endpoint para obter o token
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Endpoint para atualizar o token
]
