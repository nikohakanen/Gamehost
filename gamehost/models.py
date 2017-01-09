from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    developer_status = models.BooleanField(default=False)


class Game(models.Model):
    category = models.TextField()
    developer = models.OneToOneField(SiteUser, on_delete=models.CASCADE)


class Highscore(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


class Transaction(models.Model):
    player = models.ForeignKey(SiteUser)
    game = models.ForeignKey(Game)
    date = models.DateField(auto_now=False, auto_now_add=True)


class Savedata(models.Model):
    player = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    data = models.TextField()
