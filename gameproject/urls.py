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

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),    # Authentication urls
    url(r'^$', views.homeview, name="homeview"),
    url(r'^home/$', views.homeview, name="homeview"),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/profile/(?P<user_id>[0-9]+)/$', views.profile),
    url(r'^register/$', views.register),
    url(r'^activate/(?P<key>.*)/?$', views.activate),
    url(r'^logout_page/', views.logout_view),
    url(r'^game/(?P<game_id>[0-9]+)/$', views.game),
    url(r'^addscore/$', views.add_highscore),
    #url(r'^index/', include('gamehost.urls')),
]
