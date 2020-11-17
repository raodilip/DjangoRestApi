from .views import article_list, article_detail
from django.urls import path

urlpatterns = [
   path('article/', article_list),
   path('detail/<int:pk>', article_detail),
]