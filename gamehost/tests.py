from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from gamehost.models import Game
from gamehost.models import Highscore
# Create your tests here.


class ModelsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Initialize test users.
        kalle = User.objects.create(username="kalle12", password="1234")
        riku = User.objects.create(username="riku9", password="2345")
        lauri = User.objects.create(username="lauri45", password="haha3")
        juha = User.objects.create(username="juha88", password="tappara")

        kalle.siteuser.developer_status = False
        riku.siteuser.developer_status = False
        lauri.siteuser.developer_status = True
        juha.siteuser.developer_status = True

        kalle.save()
        riku.save()
        lauri.save()
        juha.save()

        # Initialize test games.
        chess = Game.objects.create(
            name="Chess", category='strategy', developer=lauri.siteuser)
        pingpong = Game.objects.create(
            name="Ping Pong", category='arcade', developer=lauri.siteuser)
        glock = Game.objects.create(
            name="Glock Shot", category='shooting', developer=juha.siteuser)
        mario = Game.objects.create(
            name="Super Mario", category='adventure', developer=lauri.siteuser)

        chess.save()
        pingpong.save()
        glock.save()
        mario.save()

        # Initalize test highscores
        high1 = Highscore.objects.create(
            player=kalle.siteuser,
            game=mario,
            score="9900"
        )
        high2 = Highscore.objects.create(
            player=kalle.siteuser,
            game=mario,
            score="11000"
        )
        high3 = Highscore.objects.create(
            player=kalle.siteuser,
            game=pingpong,
            score="290"
        )
        high4 = Highscore.objects.create(
            player=riku.siteuser,
            game=mario,
            score="10120"
        )
        high5 = Highscore.objects.create(
            player=riku.siteuser,
            game=pingpong,
            score="400"
        )
        high6 = Highscore.objects.create(
            player=riku.siteuser,
            game=glock,
            score="900"
        )

        high1.save()
        high2.save()
        high3.save()
        high4.save()
        high5.save()
        high6.save()

    def test_developer_status(self):
        kalle = User.objects.get(username="kalle12")
        lauri = User.objects.get(username="lauri45")

        self.assertEqual(kalle.siteuser.developer_status, False)
        self.assertEqual(lauri.siteuser.developer_status, True)

    def test_developer_ownership(self):
        lauri = User.objects.get(username="lauri45")
        juha = User.objects.get(username="juha88")
        riku = User.objects.get(username="riku9")

        lauri_games = lauri.siteuser.game_set.all().order_by('name')
        juha_games = juha.siteuser.game_set.all().order_by('name')
        riku_games = riku.siteuser.game_set.all().order_by('name')

        self.assertQuerysetEqual(
            lauri_games,
            ["<Game: Chess>", "<Game: Ping Pong>", "<Game: Super Mario>"],
            ordered=True)
        self.assertQuerysetEqual(
            juha_games,
            ["<Game: Glock Shot>"],
            ordered=True)
        self.assertQuerysetEqual(
            riku_games,
            [],
            ordered=True)

    def test_highscores(self):
        kalle = User.objects.get(username="kalle12")
        riku = User.objects.get(username="riku9")
        lauri = User.objects.get(username="lauri45")

        mario = Game.objects.get(name="Super Mario")
        pong = Game.objects.get(name="Ping Pong")
        chess = Game.objects.get(name="Chess")
        glock = Game.objects.get(name="Glock Shot")

        mario_scores = mario.highscore_set.all().order_by('-score')
        pong_scores = pong.highscore_set.all().order_by('-score')
        chess_scores = chess.highscore_set.all().order_by('-score')
        glock_scores = glock.highscore_set.all().order_by('-score')

        self.assertQuerysetEqual(
            mario_scores,
            ["<Highscore: 11000>", "<Highscore: 10120>", "<Highscore: 9900>"],
            ordered=True)
        self.assertQuerysetEqual(
            pong_scores,
            ["<Highscore: 400>", "<Highscore: 290>"],
            ordered=True)
