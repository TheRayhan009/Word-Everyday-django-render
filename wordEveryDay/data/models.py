from django.db import models
from django.utils import timezone
from datetime import datetime

class Users(models.Model):
    # Uname=models.CharField(max_length=100)
    # Lname=models.CharField(max_length=100)
    username = models.CharField(max_length=255)
    Email = models.CharField(max_length=255,null=True)
    password=models.CharField(max_length=200)
    Last_word=models.CharField(max_length=1000,default="run")
    Last_word_date=models.DateField(default=datetime.now)

    
    def __str__(self):
        return self.username
    
