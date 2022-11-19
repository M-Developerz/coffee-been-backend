from django.urls import path, include
from rest_framework import routers
from authentication import api_views as authentication_api_views

router = routers.DefaultRouter()
router.register(r'users', authentication_api_views.UserAPIView)

urlpatterns = [
    path('', include(router.urls)),
]
