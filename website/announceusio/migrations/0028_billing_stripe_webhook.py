# Generated by Django 2.1.5 on 2019-03-16 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announceusio', '0027_stripe'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='stripe_webhook',
            field=models.CharField(default='https://cookstart.io/stripe/webhooks/', max_length=512),
        ),
    ]