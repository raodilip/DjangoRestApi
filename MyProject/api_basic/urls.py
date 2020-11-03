from .views import article_list
from django.urls import path

urlpatterns = [
   path('article/', article_list),
]