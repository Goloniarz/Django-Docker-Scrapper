from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Cars
from .serializers import CarSerializer
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .scraper import get_html, parse_page
import httpx

def index(request):
    baseurl = "https://ucars.pro/pl/sales-history/porsche?model=macan%20s"
    context = {'cars_list': []}
    if request.method == 'POST':
        num_pages = int(request.POST.get('num_pages', 1))

        for page in range(1, num_pages + 1):
            html = get_html(baseurl, params={'page': page})
            if html:
                cars = parse_page(html)
                context['cars_list'].extend(cars)
                for car in cars:
                    response = httpx.post("http://127.0.0.1:8000/api/cars/", json=car)
                    if response.status_code != 201:
                        print(f"Błąd przy dodawaniu pojazdu: {response.status_code}, {response.text}")
    else:
        context['num_pages'] = 1
    return render(request, "cars/index.html", context)

def prometheus_metrics_view(request):
    metrics = generate_latest()
    return HttpResponse(metrics, content_type=CONTENT_TYPE_LATEST)

class CarViewSet(viewsets.ModelViewSet):
    queryset = Cars.objects.all()
    serializer_class = CarSerializer
