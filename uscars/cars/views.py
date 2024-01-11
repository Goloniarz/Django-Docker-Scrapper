from django.shortcuts import render
from .scraper import get_html, parse_page
from django.http import HttpResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

def index(request):
    baseurl = "https://ucars.pro/pl/sales-history/porsche?model=macan%20s"
    context = {'cars_list': []}
    if request.method == 'POST':
        num_pages = int(request.POST.get('num_pages', 1))

        for page in range(1, num_pages + 1):
            html = get_html(baseurl, params={'page': page})
            if html:
                context['cars_list'].extend(parse_page(html))
    else:
        context['num_pages'] = 1
    return render(request, "cars/index.html", context)
def prometheus_metrics_view(request):

    metrics = generate_latest()
    return HttpResponse(metrics, content_type=CONTENT_TYPE_LATEST)
