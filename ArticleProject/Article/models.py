from django.db import models
DEFAULT_USER_ID = 1
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    email =  models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='articles', on_delete=models.CASCADE,default=DEFAULT_USER_ID)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)    