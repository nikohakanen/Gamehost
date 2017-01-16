from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class SiteUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    developer_status = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now=False, auto_now_add=True)

    def get_transactions(self):
        transactions = Transaction.objects.filter(player=self)
        return transactions

    # How to handle the money?
    def purchase_game(self, game):
        Transaction.objects.create(
            player=self,
            game=game,
            price=game.price
        )


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
        player_save = self.savedata_set.filter(player=user)
        if player_save.count() > 0:
            player_save.update(data=data)
        else:
            Savedata.objects.create(player=user, game=self, data=data)

    def get_transactions(self):
        return Transaction.objects.filter(game=self)

    def __str__(self):
        return "{}".format(self.name)


class Highscore(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "{}".format(self.score)


class Transaction(models.Model):
    player = models.ForeignKey(SiteUser)
    game = models.ForeignKey(Game)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "{}".format(self.game)


class Savedata(models.Model):
    player = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    data = models.TextField()
    date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return "{}".format(self.data)
