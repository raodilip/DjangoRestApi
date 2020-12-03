from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GenericAPIViewArticleList (generics.GenericAPIView , 
     mixins.ListModelMixin , mixins.CreateModelMixin):
      serializer_class = ArticleSerializer
      queryset = Article.objects.all()
      authentication_classes = [SessionAuthentication, BasicAuthentication]
      permission_classes = [IsAuthenticated]


      def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

      def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)   


class ArticleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        # return JsonResponse(serializer.data, safe = False)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        # print("request data",request.data)
        # data = JSONParser().parse(request)
        # data = json.loads(request.data)
        # print(data)
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data ,status=201)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors ,status=400)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ArticleDetails(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
        # return HttpResponse(status=404)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self , request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        # return JsonResponse(serializer.data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

    def delete(self, request, pk, format=None):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     

class GenericAPIViewArticleDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Create your views here.
#@csrf_exempt
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        # return JsonResponse(serializer.data, safe = False)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data ,status=201)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors ,status=400)
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)    

# @csrf_exempt
@api_view(['GET','PUT','DELETE'])
def article_detail(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        # return HttpResponse(status=404)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    if request.method == "GET":
        serializer = ArticleSerializer(article)
        # return JsonResponse(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        # data = JSONParser().parse(request)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data ,status=201)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        # return JsonResponse(serializer.errors ,status=400) 
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        article.delete()
        # return HttpResponse(status = 204)
        return Response(status=status.HTTP_204_NO_CONTENT)
