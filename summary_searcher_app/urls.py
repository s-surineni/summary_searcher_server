from django.urls import path

from .views import search_summaries_view


urlpatterns = [
    path('search-summaries/', search_summaries_view),
]
