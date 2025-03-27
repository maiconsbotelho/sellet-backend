from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServicoViewSet

router = DefaultRouter()
router.register(r'', ServicoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
