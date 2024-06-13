from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CarViewSet

router = DefaultRouter()
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('', include(router.urls)),
     path('api/', include(router.urls)),
]