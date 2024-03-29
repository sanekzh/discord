# Generated by Django 2.1.5 on 2019-01-11 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announceusio', '0010_auto_20190111_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='discord_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='discord_username',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='bot_token',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='discord_channel_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='discord_server_id',
            field=models.CharField(default='asds', max_length=255),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='email_password',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='item_name',
            field=models.CharField(default='announceus.io - PREMIUM', max_length=255),
        ),
    ]
