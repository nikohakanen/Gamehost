"""gameproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from gamehost import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, name="login"),
    url(r'^logout/$', auth_views.logout, {'next_page': r'/home/'}, name="logout"),
    url(r'^$', views.homeview, name="homeview"),
    url(r'^home/$', views.homeview, name="homeview"),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/profile/(?P<user_id>[0-9]+)/$', views.profile),
    url(r'^register/$', views.register),
    url(r'^activate/(?P<key>.*)/?$', views.activate),
    url(r'^game/(?P<game_id>[0-9]+)/$', views.game),
    url(r'^add_game/$', views.add_game),
    url(r'^addscore/$', views.add_highscore),
    url(r'^savegame/$', views.save_game),
    url(r'^loadgame/$', views.load_game),
    url(r'^editgame/(?P<game_id>[0-9]+)/$', views.edit_game),
    url(r'^deletegame/(?P<game_id>[0-9]+)/$', views.delete_game),
    url(r'^add_to_basket/(?P<game_id>[0-9]+)/$', views.add_to_basket, name="add_to_basket"),
    url(r'^remove_from_basket/(?P<game_id>[0-9]+)/$', views.remove_from_basket, name="remove_from_basket"),
    url(r'^basket/$', views.basket, name="basket"),
    url(r'^purchased_games/(?P<user_id>[0-9]+)/$', views.purchased_games),
    url(r'^games/$', views.games),
    url(r'^checkout/$', views.checkout, name="checkout"),
    url(r'^checkout/success/$', views.payment_success, name="payment_success"),
    url(r'^checkout/cancel/$', views.payment_cancel, name="payment_cancel"),
    url(r'^checkout/error/$', views.payment_error, name="payment_error"),
    url(r'^checkout/lost/$', views.payment_lost, name="payment_lost"),
    url(r'', include('social_django.urls', namespace='social')),
]
