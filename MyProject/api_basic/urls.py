from .views import article_list, article_detail ,ArticleAPIView, ArticleDetails
from django.urls import path

urlpatterns = [
   # path('article/', article_list),
   path('article/', ArticleAPIView.as_view()),
   # path('detail/<int:pk>', article_detail),
   path('detail/<int:pk>', ArticleDetails.as_view()),
]