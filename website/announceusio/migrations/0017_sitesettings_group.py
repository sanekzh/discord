# Generated by Django 2.1.5 on 2019-02-22 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('announceusio', '0016_member_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='group',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='auth.Group'),
        ),
    ]