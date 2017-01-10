from django.test import TestCase
from django.contrib.auth.models import User
from gamehost.models import SiteUser
from django.test import Client

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

    def test_developer_status(self):
        kalle = User.objects.get(username="kalle12")
        lauri = User.objects.get(username="lauri45")

        self.assertEqual(kalle.siteuser.developer_status, False)
        self.assertEqual(lauri.siteuser.developer_status, True)
