from .views import article_list, article_detail ,ArticleAPIView, ArticleDetails, GenericAPIViewArticleList, GenericAPIViewArticleDetail
from django.urls import path

urlpatterns = [
   # path('article/', article_list),
   path('generic/article/', GenericAPIViewArticleList.as_view()),
   path('generic/articleDetail/<int:pk>', GenericAPIViewArticleDetail.as_view()),
   path('article/', ArticleAPIView.as_view()),
   # path('detail/<int:pk>', article_detail),
   path('detail/<int:pk>', ArticleDetails.as_view()),
]