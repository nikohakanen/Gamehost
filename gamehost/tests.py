from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from gamehost.models import Game
from gamehost.models import Highscore
from gamehost.models import Savedata
from gamehost.models import Transaction

from gamehost.forms import UserForm, SiteUserForm
from django.core import mail
# Create your tests here.


class ModelsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Initialize test users.
        kalle = User.objects.create(username="kalle12", password="1234")
        riku = User.objects.create(username="riku9", password="2345")
        lauri = User.objects.create(username="lauri45", password="haha3")
        juha = User.objects.create(username="juha88", password="tappara")

        lauri.siteuser.developer_status = True
        juha.siteuser.developer_status = True
        # kalle and riku should default to False

        kalle.save()
        riku.save()
        lauri.save()
        juha.save()

        # Initialize test games.
        chess = Game.objects.create(
            name="Chess", category='strategy',
            developer=lauri.siteuser, src="www.chess.lol",
            price=2.99)
        pingpong = Game.objects.create(
            name="Ping Pong", category='arcade',
            developer=lauri.siteuser, src="www.pingpong.lol",
            price=5.00)
        glock = Game.objects.create(
            name="Glock Shot", category='shooting',
            developer=juha.siteuser, src="www.glock.lol",
            price=3.50)
        mario = Game.objects.create(
            name="Super Mario", category='adventure',
            developer=lauri.siteuser, src="www.mario.lol",
            price=12.99)

        chess.save()
        pingpong.save()
        glock.save()
        mario.save()

    def test_developer_status(self):
        kalle = User.objects.get(username="kalle12")
        lauri = User.objects.get(username="lauri45")

        # Tests that the developer statuses are correct.
        self.assertEqual(kalle.siteuser.developer_status, False)
        self.assertEqual(lauri.siteuser.developer_status, True)

    def test_developer_ownership(self):
        lauri = User.objects.get(username="lauri45")
        juha = User.objects.get(username="juha88")
        riku = User.objects.get(username="riku9")

        lauri_games = lauri.siteuser.game_set.all().order_by('name')
        juha_games = juha.siteuser.game_set.all().order_by('name')
        riku_games = riku.siteuser.game_set.all().order_by('name')

        # Tests that the games belong to their right owners.
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

    def test_highscores_lists(self):
        kalle = User.objects.get(username="kalle12")
        riku = User.objects.get(username="riku9")
        lauri = User.objects.get(username="lauri45")

        mario = Game.objects.get(name="Super Mario")
        pong = Game.objects.get(name="Ping Pong")
        chess = Game.objects.get(name="Chess")
        glock = Game.objects.get(name="Glock Shot")
        # Remove old highscore entries
        Highscore.objects.all().delete()

        # Initalize test highscores
        high1 = Highscore.objects.create(
            player=kalle.siteuser,
            game=mario,
            score=9900
        )
        high2 = Highscore.objects.create(
            player=kalle.siteuser,
            game=mario,
            score=11000
        )
        high3 = Highscore.objects.create(
            player=kalle.siteuser,
            game=pong,
            score=290
        )
        high4 = Highscore.objects.create(
            player=riku.siteuser,
            game=mario,
            score=10120
        )
        high5 = Highscore.objects.create(
            player=riku.siteuser,
            game=pong,
            score=400
        )
        high6 = Highscore.objects.create(
            player=riku.siteuser,
            game=glock,
            score=900
        )

        high1.save()
        high2.save()
        high3.save()
        high4.save()
        high5.save()
        high6.save()

        mario_scores = mario.highscore_set.all().order_by('-score')
        pong_scores = pong.highscore_set.all().order_by('-score')
        chess_scores = chess.highscore_set.all().order_by('-score')
        glock_scores = glock.highscore_set.all().order_by('-score')

        kalle_scores = kalle.siteuser.highscore_set.all().order_by('-score')
        riku_scores = riku.siteuser.highscore_set.all().order_by('-score')
        lauri_scores = lauri.siteuser.highscore_set.all().order_by('-score')

        # Tests that right highscores are pointing to right games.
        self.assertQuerysetEqual(
            mario_scores,
            ["<Highscore: 11000>", "<Highscore: 10120>", "<Highscore: 9900>"],
            ordered=True)
        self.assertQuerysetEqual(
            pong_scores,
            ["<Highscore: 400>", "<Highscore: 290>"],
            ordered=True)
        self.assertQuerysetEqual(
            chess_scores,
            [],
            ordered=True)
        self.assertQuerysetEqual(
            glock_scores,
            ["<Highscore: 900>"],
            ordered=True)

        # Tests that right highscores are earned by right users.
        self.assertQuerysetEqual(
            kalle_scores,
            ["<Highscore: 11000>", "<Highscore: 9900>", "<Highscore: 290>"],
            ordered=True)
        self.assertQuerysetEqual(
            riku_scores,
            ["<Highscore: 10120>", "<Highscore: 900>", "<Highscore: 400>"],
            ordered=True)
        self.assertQuerysetEqual(
            lauri_scores,
            [],
            ordered=True)

    def test_adding_highscores(self):
        kalle = User.objects.get(username="kalle12")

        mario = Game.objects.get(name="Super Mario")

        # Remove all old highscores, so they don't mess up this test.
        Highscore.objects.all().delete()

        # Initialize new highscores.
        high1 = Highscore.objects.create(
            player=kalle.siteuser,
            game=mario,
            score=9900
        )
        high2 = Highscore.objects.create(
            player=kalle.siteuser,
            game=mario,
            score=11000
        )
        high3 = Highscore.objects.create(
            player=kalle.siteuser,
            game=mario,
            score=290
        )
        high4 = Highscore.objects.create(
            player=kalle.siteuser,
            game=mario,
            score=10120
        )

        high1.save()
        high2.save()
        high3.save()
        high4.save()

        # Check that there really is only four highscores.
        self.assertEqual(mario.highscore_set.count(), 4)

        # Add a new highscore, and check that it is added.
        mario.addHighscore(200, kalle.siteuser)
        self.assertEqual(mario.highscore_set.count(), 5)
        self.assertQuerysetEqual(
            mario.highscore_set.all().order_by('score'),
            ["<Highscore: 200>", "<Highscore: 290>", "<Highscore: 9900>",
                "<Highscore: 10120>", "<Highscore: 11000>"],
            ordered=True)

        # Try adding a sixth highscore to same user, and see that it is not
        # added.

        # Remove comments if there is to be a limit!!!
        """
        mario.addHighscore(100, kalle.siteuser)
        self.assertEqual(mario.highscore_set.count(), 5)
        self.assertQuerysetEqual(
             mario.highscore_set.all().order_by('score'),
             ["<Highscore: 200>", "<Highscore: 290>", "<Highscore: 9900>",
              "<Highscore: 10120>", "<Highscore: 11000>"],
             ordered=True)

        # Add a new highscore to someone else, and see that it is counted
        # properly.
        mario.addHighscore(50, riku.siteuser)
        self.assertEqual(mario.highscore_set.count(), 6)
        self.assertQuerysetEqual(
             mario.highscore_set.all().order_by('score'),
             ["<Highscore: 50>", "<Highscore: 200>", "<Highscore: 290>",
                 "<Highscore: 9900>", "<Highscore: 10120>",
                 "<Highscore: 11000>"],
             ordered=True)

        # Add a new, better highscore to someone with already five highscores.
        # See that the smallest is removed.
        mario.addHighscore(400, kalle.siteuser)
        self.assertEqual(mario.highscore_set.count(), 6)
        self.assertQuerysetEqual(
            mario.highscore_set.all().order_by('score'),
            ["<Highscore: 50>", "<Highscore: 290>", "<Highscore: 400>",
                "<Highscore: 9900>", "<Highscore: 10120>",
                "<Highscore: 11000>"],
            ordered=True)
        """

    def test_save_data(self):
        kalle = User.objects.get(username="kalle12")
        riku = User.objects.get(username="riku9")

        mario = Game.objects.get(name="Super Mario")
        # Delete earlier savedata entries so they don't mess up this test.
        Savedata.objects.all().delete()

        # Initialize new Savedata entry.
        Savedata.objects.create(
            player=kalle.siteuser,
            game=mario,
            data="100010101010111001010"
        )

        kalle_saves = kalle.siteuser.savedata_set.all()
        riku_saves = riku.siteuser.savedata_set.all()

        # Test that there are correct savedatas after initialization.
        self.assertEqual(kalle_saves.count(), 1)
        self.assertEqual(riku_saves.count(), 0)
        self.assertQuerysetEqual(
            kalle_saves,
            ["<Savedata: 100010101010111001010>"])

    def test_save_game_data(self):
        kalle = User.objects.get(username="kalle12")
        riku = User.objects.get(username="riku9")

        mario = Game.objects.get(name="Super Mario")
        # Delete earlier savedata entries to they don't mess up this test.
        Savedata.objects.all().delete()

        # Initialize new savedata entry.
        Savedata.objects.create(
            player=kalle.siteuser,
            game=mario,
            data="100010101010111001010"
        )
        # Call savedata. Since there already is an entry, it should be updated.
        mario.saveGame(kalle.siteuser, "1010101010")
        self.assertEqual(kalle.siteuser.savedata_set.count(), 1)
        self.assertQuerysetEqual(
            kalle.siteuser.savedata_set.all(),
            ["<Savedata: 1010101010>"])

        # Test that riku has initially 0 entries.
        self.assertEqual(riku.siteuser.savedata_set.count(), 0)
        # Call saveGame. Since there were no earlier entries, a new one should
        # be created.
        mario.saveGame(riku.siteuser, "10000000000")
        self.assertEqual(riku.siteuser.savedata_set.count(), 1)
        self.assertQuerysetEqual(
            riku.siteuser.savedata_set.all(),
            ["<Savedata: 10000000000>"]
        )

    def test_transactions(self):
        kalle = User.objects.get(username="kalle12")
        riku = User.objects.get(username="riku9")

        mario = Game.objects.get(name="Super Mario")
        chess = Game.objects.get(name="Chess")
        pong = Game.objects.get(name="Ping Pong")

        # Delete all existing transactions so they don't interfere with this
        # test.
        Transaction.objects.all().delete()

        # Create a couple transactions.
        trans1 = Transaction.objects.create(
            player=kalle.siteuser,
            game=mario,
            price=mario.price
        )
        trans2 = Transaction.objects.create(
            player=kalle.siteuser,
            game=chess,
            price=chess.price
        )

        trans1.save()
        trans2.save()

        self.assertEqual(kalle.siteuser.transaction_set.count(), 2)
        self.assertEqual(riku.siteuser.transaction_set.count(), 0)
        self.assertEqual(mario.transaction_set.count(), 1)
        self.assertEqual(pong.transaction_set.count(), 0)
        kalle_transactions = kalle.siteuser.get_transactions()
        self.assertQuerysetEqual(
            kalle_transactions,
            ["<Transaction: Super Mario>", "<Transaction: Chess>"],
            ordered=False
        )
        self.assertQuerysetEqual(
            riku.siteuser.get_transactions(),
            [],
            ordered=False
        )
        self.assertQuerysetEqual(
            mario.get_transactions(),
            ["<Transaction: Super Mario>"],
            ordered=False
        )
        self.assertQuerysetEqual(
            pong.get_transactions(),
            [],
            ordered=False
        )

    def test_purchase(self):
        kalle = User.objects.get(username="kalle12")
        mario = Game.objects.get(name="Super Mario")

        # Remove existing transactions.
        Transaction.objects.all().delete()

        self.assertEqual(kalle.siteuser.transaction_set.count(), 0)

        kalle.siteuser.purchase_game(mario)
        self.assertEqual(kalle.siteuser.transaction_set.count(), 1)

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register(self):
        response1 = self.client.post('/register/', {'user-username': 'Dean', 'user-password': 'secret', 'user-email': 'dean@dena.fi', 'siteuser-developer_status': True})

        user = User.objects.get(username='Dean')

        #Test that user is not active yet, he was redirected to the right page, and that the activation email was sent
        self.assertEqual(user.is_active, False)
        self.assertEqual(response1.templates[0].name, 'message.html')
        self.assertEqual(mail.outbox[0].subject, 'Your activation link')

        #Test that you can't login before activating the account
        response2 = self.client.post('/login/', {'username': 'Dean', 'password': 'secret'})
        self.assertFormError(response2, 'form', None, 'This account is inactive.', msg_prefix='')

        #Get the activation link from the email message
        parts = mail.outbox[0].body.split('testserver')
        path = parts[1]

        response3 = self.client.get(path)
        #print(response2.content)
        #Check that is user is now active
        user = User.objects.get(username='Dean')
        self.assertEqual(user.is_active, True)

    def test_login(self):
        pass
