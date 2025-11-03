from django.urls import path
from django.http import JsonResponse
from .views import GolfSearchView


def health(request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('api/health/', health),
    path('api/golf-search/', GolfSearchView.as_view()),
]
