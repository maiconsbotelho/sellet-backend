from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet

router = DefaultRouter()
router.register(r'', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Não é necessário o prefixo 'api/' aqui
]
