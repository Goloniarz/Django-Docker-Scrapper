
from django.urls import path, include
from django.contrib import admin
from django.http import HttpResponse
from cars.views import prometheus_metrics_view

def home(request):
    return HttpResponse("Welcome")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cars.urls')),
    path('metrics', prometheus_metrics_view, name='prometheus-metrics'),
]
