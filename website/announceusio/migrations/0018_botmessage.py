# Generated by Django 2.1.5 on 2019-03-05 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('announceusio', '0017_botsettings_member_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_message_body', models.TextField(default='\n        ``` Supported commands:\n        !activate example@example.com - you activate your membershp.\n        !renew - you get membership renewal link.\n        !status - gives days left before expiration.\n        !help - show help message.\n        ```\n\n        ')),
                ('wrong_email', models.TextField(default='This is not your email. You have been activated with a different email.')),
                ('already_activated', models.TextField(default='You are already activated! ')),
                ('activated', models.TextField(default='You have been activated! {}')),
                ('before_expiration', models.TextField(default='You have {} hours left before expiration!')),
                ('should_activate', models.TextField(default='You should activate your membership with command !activate example@example.com')),
                ('renewal_link', models.TextField(default='Renewal link http://announceus.io/renew/?email={}')),
                ('buy_membership', models.TextField(default='Please buy membership http://announceus.io')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
