# Generated by Django 2.1.5 on 2019-02-27 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announceusio', '0016_auto_20190226_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='botsettings',
            name='member_role',
            field=models.CharField(default='Member', max_length=255),
        ),
    ]
