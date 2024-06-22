from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tags(models.Model):
    title=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.title

class Snippet(models.Model):
    title = models.CharField(max_length=100)
    note = models.TextField()
    created= models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE,related_name='snippets')
    tags = models.ManyToManyField(Tags, related_name='snippets')

    def __str__(self):
        return self.title
