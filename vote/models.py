from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE)
    ip = models.CharField(max_length=200)
    
    def __str__(self):
        return self.question_text
        

class Choices(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    ip = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', related_name='choices', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.choice_text
    