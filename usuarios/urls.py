from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'', UserProfileViewSet)

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Endpoint de login
    path('', include(router.urls)),
]