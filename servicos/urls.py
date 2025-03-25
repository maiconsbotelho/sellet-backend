from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServicoViewSet

router = DefaultRouter()
router.register(r'servicos', ServicoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
