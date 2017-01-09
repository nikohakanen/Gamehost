from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    developer_status = models.BooleanField(default=False)

class Game(models.Model):
    category = models.TextField()

class Highscore(models.Model):
    pass

class Transaction(models.Model):
    pass

class Savedata(models.Model):
    pass


    
