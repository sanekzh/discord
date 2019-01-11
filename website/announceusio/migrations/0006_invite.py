# Generated by Django 2.1.5 on 2019-01-11 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announceusio', '0005_auto_20190111_0627'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=300, null=True, unique=True)),
                ('is_invited', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
