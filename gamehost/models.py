from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.files.storage import get_storage_class
from django.conf import settings
import json

# Create your models here.


class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    developer_status = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now=False, auto_now_add=True)

    def get_transactions(self):
        transactions = Transaction.objects.filter(player=self, payment__status=Payment.SUCCESS)
        return transactions

    def has_purchased_game(self, game):
        query = Transaction.objects.filter(player=self, game=game, payment__status=Payment.SUCCESS)
        if query.count() >= 1:
            return True
        else:
            return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        SiteUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_siteuser(sender, instance, **kwards):
    instance.siteuser.save()


class Game(models.Model):
    name = models.TextField()

    UNDEFINED = 'undefined'
    STRATEGY = 'strategy'
    SHOOTING = 'shooting'
    ARCADE = 'arcade'
    ADVENTURE = 'adventure'
    CATEGORY_CHOICES = (
        (UNDEFINED, 'undefined'),
        (STRATEGY, 'strategy'),
        (SHOOTING, 'shooting'),
        (ARCADE, 'arcade'),
        (ADVENTURE, 'adventure')
    )
    category = models.TextField(
        choices=CATEGORY_CHOICES,
        default=UNDEFINED
    )
    developer = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    src = models.URLField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    publish_date = models.DateField(auto_now=False, auto_now_add=True)
    thumbnail = models.URLField(
        null=True,
        blank=True
    )

    def addHighscore(self, score, user):
        # Remove comments if the amount of highscores is to be limited.
        # player_scores = self.highscore_set.filter(
        #    player=user).order_by('score')
        # if player_scores.count() >= 5:
        #    if (score > player_scores.first().score):
        #        player_scores.first().delete()
        #        Highscore.objects.create(player=user, game=self, score=score)
        # else:
            Highscore.objects.create(player=user, game=self, score=score)

    def saveGame(self, user, data):
        try:
            save = Savedata.objects.get(player=user, game=self)
            save.data = data
            save.save()
            return save
        except Savedata.DoesNotExist:
            save = Savedata()
            save.player = user
            save.game = self
            save.data = data
            save.save()
            return save

    def loadGame(self, user):
        try:
            load = Savedata.objects.get(player=user, game=self)
            data = json.loads(load.data)
            return data
        except Savedata.DoesNotExist:
            msg = "No data found"
            return msg

    def get_transactions(self):
        return Transaction.objects.filter(game=self, payment__status=Payment.SUCCESS)

    def get_highscores(self, user, own):
        if (own):
            query_set = Highscore.objects.filter(game=self, user=user)
        else:
            query_set = Highscore.objects.filter(
                game=self).order_by('-score')[:5]
        if query_set.count() > 5:
            return query_set[:5]
        else:
            return query_set

    def __str__(self):
        return "{}".format(self.name)


class Highscore(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "{}".format(self.score)


class Payment(models.Model):
    # Failed payments will be deleted
    IN_PROGRESS = 'in_progress'
    SUCCESS = 'success'
    STATUS_CHOICES = (
        (IN_PROGRESS, 'in_progress'),
        (SUCCESS, 'success'),
    )
    status = models.TextField(
        choices=STATUS_CHOICES,
        default=IN_PROGRESS
    )
    date = models.DateField(auto_now=False, auto_now_add=True)
    total = models.DecimalField(decimal_places=2, max_digits=9)


class Transaction(models.Model):
    player = models.ForeignKey(SiteUser)
    game = models.ForeignKey(Game)
    price = models.DecimalField(decimal_places=2, max_digits=6)

    @staticmethod
    def default_payment():
        payment = Payment.objects.create(total=0, status=Payment.SUCCESS)
        return payment.id

    payment = models.ForeignKey(Payment, default=default_payment, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.game)


class Savedata(models.Model):
    player = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    data = models.TextField()
    date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "{}".format(self.data)
