from .views import article_list, article_detail ,ArticleAPIView, ArticleDetails, GenericAPIViewArticleList, GenericAPIViewArticleDetail, UserList, UserDetail
from django.urls import path, include

urlpatterns = [
   # path('article/', article_list),
   path('generic/article/', GenericAPIViewArticleList.as_view()),
   path('generic/articleDetail/<int:pk>', GenericAPIViewArticleDetail.as_view()),
   path('article/', ArticleAPIView.as_view()),
   # path('detail/<int:pk>', article_detail),
   path('detail/<int:pk>', ArticleDetails.as_view()),
   path('users/', UserList.as_view()),
   path('users/<int:pk>/', UserDetail.as_view()),
]
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]