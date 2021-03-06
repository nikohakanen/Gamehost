# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-14 10:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
from django.contrib.auth.hashers import make_password
import django.db.models.deletion
import gamehost.models


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# gamehost.migrations.0005_add_initial_data

def add_initial_data(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    User = apps.get_model("auth", "User")
    SiteUser = apps.get_model("gamehost", "SiteUser")
    user = User.objects.using(db_alias).create(username="user", password=make_password("user"))
    SiteUser.objects.using(db_alias).create(user=user)
    dev = User.objects.using(db_alias).create(username="dev", password=make_password("dev"))
    SiteUser.objects.using(db_alias).create(user=dev, developer_status=True)
    admin = User.objects.using(db_alias).create(username="admin", password=make_password("admin"),
                                                is_superuser=True, is_staff=True)
    SiteUser.objects.using(db_alias).create(user=admin, developer_status=True)

    Game = apps.get_model("gamehost", "Game")
    one = Game.objects.using(db_alias).create(name="one", developer=dev.siteuser, price=10,
                                        src="http://webcourse.cs.hut.fi/example_game.html",
                                        thumbnail="http://placehold.it/150x150")
    two = Game.objects.using(db_alias).create(name="two", developer=dev.siteuser, price=20,
                                        src="http://webcourse.cs.hut.fi/example_game.html",
                                        thumbnail="http://placehold.it/250x250")

    Highscore = apps.get_model("gamehost", "Highscore")
    Highscore.objects.using(db_alias).create(game=one, player=user.siteuser, score=100)
    Highscore.objects.using(db_alias).create(game=one, player=user.siteuser, score=90)
    Highscore.objects.using(db_alias).create(game=one, player=dev.siteuser, score=50)
    Highscore.objects.using(db_alias).create(game=one, player=admin.siteuser, score=999999)
    Highscore.objects.using(db_alias).create(game=two, player=user.siteuser, score=200)
    Highscore.objects.using(db_alias).create(game=two, player=dev.siteuser, score=52)
    Highscore.objects.using(db_alias).create(game=two, player=admin.siteuser, score=-99)

    Payment = apps.get_model("gamehost", "Payment")
    payment1 = Payment.objects.using(db_alias).create(total=-30, status="success")

    Transaction = apps.get_model("gamehost", "Transaction")
    Transaction.objects.using(db_alias).create(game=one, player=admin.siteuser, price=-10, payment=payment1)
    Transaction.objects.using(db_alias).create(game=two, player=admin.siteuser, price=-20, payment=payment1)


def remove_initial_data(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    User = apps.get_model("auth", "User")
    User.objects.using(db_alias).filter(username="user").delete()
    User.objects.using(db_alias).filter(username="dev").delete()
    User.objects.using(db_alias).filter(username="admin").delete()


class Migration(migrations.Migration):

    replaces = [('gamehost', '0001_initial'), ('gamehost', '0002_auto_20170119_1702'), ('gamehost', '0003_game_thumbnail'), ('gamehost', '0004_auto_20170123_1204'), ('gamehost', '0005_add_initial_data'), ('gamehost', '0006_auto_20170213_1612'), ('gamehost', '0007_transaction_date'), ('gamehost', '0008_auto_20170213_1942'), ('gamehost', '0009_remove_transaction_date')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('category', models.TextField(choices=[(b'undefined', b'undefined'), (b'strategy', b'strategy'), (b'shooting', b'shooting'), (b'arcade', b'arcade'), (b'adventure', b'adventure')], default=b'undefined')),
                ('src', models.URLField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('publish_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Highscore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamehost.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Savedata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamehost.Game')),
            ],
        ),
        migrations.CreateModel(
            name='SiteUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developer_status', models.BooleanField(default=False)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamehost.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamehost.SiteUser')),
            ],
        ),
        migrations.AddField(
            model_name='savedata',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamehost.SiteUser'),
        ),
        migrations.AddField(
            model_name='highscore',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamehost.SiteUser'),
        ),
        migrations.AddField(
            model_name='game',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamehost.SiteUser'),
        ),
        migrations.AlterField(
            model_name='game',
            name='category',
            field=models.TextField(choices=[('undefined', 'undefined'), ('strategy', 'strategy'), ('shooting', 'shooting'), ('arcade', 'arcade'), ('adventure', 'adventure')], default='undefined'),
        ),
        migrations.AddField(
            model_name='game',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(choices=[('in_progress', 'in_progress'), ('success', 'success')], default='in_progress')),
                ('date', models.DateField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='date',
        ),
        migrations.AddField(
            model_name='transaction',
            name='payment',
            field=models.ForeignKey(default=gamehost.models.default_payment, on_delete=django.db.models.deletion.CASCADE, to='gamehost.Payment'),
        ),
        migrations.RunPython(
            code=add_initial_data,
            reverse_code=remove_initial_data,
        ),
    ]
