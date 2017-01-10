from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from gamehost.models import Game
# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
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
