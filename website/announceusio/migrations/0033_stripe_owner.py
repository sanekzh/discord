# Generated by Django 2.1.5 on 2019-04-09 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('announceusio', '0032_billing_stripe_secret_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripe',
            name='owner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]