# Generated by Django 2.1.5 on 2019-01-11 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announceusio', '0009_auto_20190111_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='paypal_email',
            field=models.EmailField(default='some@mail.com', max_length=300),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='price',
            field=models.CharField(default='25', max_length=20),
        ),
    ]
