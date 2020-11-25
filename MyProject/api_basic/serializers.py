from rest_framework import serializers
from .models import Article
from django.contrib.auth.models import User

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ['id','title','author','owner']

class UserSerializer(serializers.ModelSerializer):
    articles = serializers.PrimaryKeyRelatedField(many=True, queryset=Article.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'articles']        
        
    # title = serializers.CharField(max_length=100)
    # author = serializers.CharField(max_length=100)
    # email =  serializers.EmailField(max_length=100)
    # date = serializers.DateTimeField()  

    # def create(self,validated_data):
    #     return Article.objects.create(validated_data)

    # def update(self, instance,validated_data):
    #     instance.title = validated_data.get('title',instance.title)
    #     instance.author = validated_data.get('title',instance.author)
    #     instance.email = validated_data.get('title',instance.email)
    #     instance.date = validated_data.get('title',instance.date)
